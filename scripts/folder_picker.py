
import os
import sys
from pathlib import Path
from nicegui import ui

class FolderPicker(ui.card):
    def __init__(self, directory, on_select, on_cancel):
        super().__init__()
        self.path = Path(directory).expanduser()
        self.path_str = str(self.path) # Initialize for binding
        self.on_select = on_select
        self.on_cancel = on_cancel
        self.drives = self.get_drives()
        
        with self.classes('w-[500px] h-[600px] flex flex-col p-0 gap-0 overflow-hidden rounded-xl bg-[#1e1e1e] border border-gray-700 shadow-2xl'):
            # Header
            with ui.row().classes('w-full p-4 bg-[#252525] border-b border-gray-700 items-center justify-between'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('folder_open').classes('text-blue-400')
                    ui.label('Explorador de Carpetas').classes('font-bold text-gray-200')
                ui.button(icon='close', on_click=self.on_cancel).props('flat dense round color=grey')

            # Path & Navigation
            with ui.column().classes('w-full p-2 bg-[#1e1e1e] border-b border-gray-700 gap-2'):
                # Drive Selector (Windows)
                if os.name == 'nt':
                    with ui.row().classes('gap-2 items-center text-xs text-gray-400'):
                        ui.label('Unidades:')
                        for drive in self.drives:
                            ui.button(drive, on_click=lambda d=drive: self.set_path(d)).props('outline dense color=grey-5').classes('px-2 py-0 text-xs')
                
                # Breadcrumbs / Path Input
                with ui.row().classes('w-full items-center gap-2'):
                    ui.button(icon='arrow_upward', on_click=self.go_up).props('flat dense round color=grey-4').tooltip('Subir un nivel')
                    ui.input(value=str(self.path)).bind_value_to(self, 'path_str').on('keydown.enter', self.update_from_input).props('dense outlined dark input-class="text-gray-300"').classes('flex-grow font-mono text-sm')
                    ui.button(icon='refresh', on_click=self.render_files).props('flat dense round color=blue-4')

            # File List
            self.scroll = ui.scroll_area().classes('flex-grow w-full bg-[#1e1e1e] relative')
            
            # Footer
            with ui.row().classes('w-full p-4 bg-[#252525] border-t border-gray-700 justify-between items-center'):
                ui.label().bind_text_from(self, 'path', lambda p: f'Seleccionado: {p.name or p}').classes('text-xs text-gray-400 truncate max-w-[200px]')
                with ui.row().classes('gap-2'):
                    ui.button('Cancelar', on_click=self.on_cancel).props('flat color=grey')
                    ui.button('Seleccionar Esta Carpeta', on_click=lambda: self.on_select(str(self.path))).classes('bg-blue-600 text-white shadow-md hover:bg-blue-500')

        self.render_files()

    def get_drives(self):
        drives = []
        if os.name == 'nt':
            import string
            from ctypes import windll
            bitmask = windll.kernel32.GetLogicalDrives()
            for letter in string.ascii_uppercase:
                if bitmask & 1:
                    drives.append(f'{letter}:\\')
                bitmask >>= 1
        else:
            drives.append('/')
        return drives

    def set_path(self, new_path):
        self.path = Path(new_path)
        self.render_files()

    def go_up(self):
        if self.path.parent != self.path:
            self.path = self.path.parent
        self.render_files()

    def update_from_input(self, e=None):
        p = Path(self.path_str)
        if p.exists() and p.is_dir():
            self.path = p
            self.render_files()
        else:
            ui.notify('Ruta inválida', type='warning')

    def render_files(self):
        self.scroll.clear()
        self.path_str = str(self.path)
        
        with self.scroll:
            with ui.list().props('dense separator').classes('w-full'):
                # Folders
                try:
                    # Scan directory
                    items = sorted([p for p in self.path.iterdir()], key=lambda i: (not i.is_dir(), i.name.lower()))
                    
                    if not items:
                        ui.label('(Carpeta vacía)').classes('text-gray-500 p-4 italic text-sm text-center w-full')

                    for item in items:
                        if item.is_dir():
                            # Folder Item
                            with ui.item(on_click=lambda i=item: self.set_path(i)).classes('hover:bg-[#2a2a2a] cursor-pointer text-gray-300'):
                                with ui.item_section().props('avatar'):
                                    ui.icon('folder', color='yellow-8').classes('opacity-80')
                                with ui.item_section():
                                    ui.item_label(item.name).classes('text-gray-200')
                        # Optional: Show files? NO, only folders relevant for scanning? 
                        # User wants Scan Recursive, usually selects a root.
                        # Maybe show files as disabled text to give context?
                        # Let's hide files to keep it clean for "Folder Selection" mode
                        
                except PermissionError:
                    with ui.column().classes('w-full items-center p-8'):
                        ui.icon('lock', size='32px').classes('text-red-400')
                        ui.label('Acceso Denegado').classes('text-red-500 font-bold')
                except Exception as e:
                    ui.label(f'Error: {e}').classes('text-red-500 p-4')
