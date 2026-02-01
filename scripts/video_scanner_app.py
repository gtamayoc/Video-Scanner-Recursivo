"""
Aplicación Visual de Escaneo Recursivo de Videos
Interfaz NiceGUI rediseñada con estética moderna y estados definidos
"""

import os
import sys
import asyncio
import time
from pathlib import Path
from typing import List, Optional

# Agregar ruta de scripts
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from nicegui import ui, app
from video_scanner import VideoScanner, VideoInfo, formatear_duracion, formatear_tamano
from folder_picker import FolderPicker

# Configuración de estilos globales
APP_FONT = 'Inter'
# PRIMARY_COLOR = '#2563EB'  # blue-600

class VideoScannerApp:
    """
    Aplicación principal con gestión de estados para la UI:
    - Initial: Selección de carpeta
    - Scanning: Progreso
    - Results: Dashboard de resultados
    """
    
    def __init__(self):
        self.scanner = VideoScanner()
        self.videos: List[VideoInfo] = []
        self.carpeta_seleccionada: Optional[str] = None
        
        # Estado de la aplicación
        self.state = 'initial'  # 'initial', 'scanning', 'results'
        
        # Variables reactivas (para bindings)
        self.progress_value = 0.0
        self.current_folder = ""
        self.scan_stats = {}
        self.time_elapsed = 0
        self.start_time = 0
        self.btn_pause = None
        
    def create_ui(self):
        """Construir la interfaz base"""
        # Configurar head para fuentes
        ui.add_head_html('''
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
            <style>
                body { font-family: 'Inter', sans-serif; background-color: #121212; color: #e0e0e0; }
                .glass-card { background: #1e1e1e; border: 1px solid #333; border-radius: 16px; box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.3); }
                .q-table__container { background-color: #1e1e1e !important; color: #e0e0e0 !important; }
                .q-table__bottom { background-color: #1e1e1e !important; border-top: 1px solid #333 !important; color: #e0e0e0 !important; }
                .q-table thead tr th { color: #e0e0e0 !important; }
            </style>
        ''')
        ui.dark_mode().enable() # Force Dark Mode
        
        ui.page_title('Video Scanner Pro')
        
        # Contenedor principal que se refresca según el estado
        @ui.refreshable
        def render_content():
            if self.state == 'initial':
                self.render_initial_state()
            elif self.state == 'scanning':
                self.render_scanning_state()
            elif self.state == 'results':
                self.render_results_state()
                
        self.render_content = render_content
        
        # Layout principal
        with ui.column().classes('w-full min-h-screen items-center justify-center p-0 m-0'):
            render_content()
            
    def render_initial_state(self):
        """Estado 1: Pantalla inicial de selección"""
        with ui.card().classes('w-full max-w-4xl h-[80vh] flex flex-col items-center justify-center glass-card p-12 relative'):
            # Header simple
            with ui.row().classes('absolute top-6 left-6 items-center gap-2'):
                ui.icon('slow_motion_video', size='24px').classes('text-gray-700')
                ui.label('Video Scanner').classes('font-semibold text-gray-700')
                
            with ui.row().classes('absolute top-6 right-6 gap-4'):
                ui.icon('settings', size='20px').classes('text-gray-400 cursor-pointer hover:text-gray-600')
                ui.icon('help_outline', size='24px').classes('text-gray-400 cursor-pointer hover:text-gray-600')

            # Contenido central
            with ui.column().classes('items-center gap-8 max-w-lg text-center'):
                # Icono grande animado
                with ui.element('div').classes('bg-blue-900/30 p-6 rounded-full mb-4 animate-bounce'):
                    ui.icon('folder_open', size='64px').classes('text-blue-500')
                
                with ui.column().classes('gap-2 items-center'):
                    ui.label('Escáner de Videos').classes('text-3xl font-bold text-gray-100')
                    ui.label('Selecciona una carpeta para comenzar el escaneo recursivo de archivos multimedia.').classes('text-gray-400 text-lg')
                
                # Area de Selección (Click)
                with ui.card().on('click', self.seleccionar_carpeta).classes('w-full border-2 border-dashed border-gray-700 bg-gray-800/50 p-10 rounded-xl hover:border-blue-500 transition-colors cursor-pointer flex flex-col items-center gap-4'):
                    ui.icon('create_new_folder', size='48px').classes('text-gray-500')
                    ui.label('Click para seleccionar carpeta').classes('font-medium text-gray-300')
                    ui.label('Explora tus directorios locales').classes('text-sm text-gray-500')
                    
                with ui.row().classes('w-full gap-2'):
                     ui.button('SELECCIONAR CARPETA', on_click=self.seleccionar_carpeta).classes(
                        'flex-grow py-3 bg-blue-600 text-white rounded-lg shadow-lg hover:bg-blue-700 hover:shadow-xl transition-all font-bold text-lg'
                     )
                
                # Input manual fallback
                with ui.expansion('Ingresar ruta manualmente', icon='edit').classes('w-full bg-transparent text-gray-400'):
                     with ui.row().classes('w-full items-center gap-2'):
                        path_input = ui.input('Ruta absoluta').props('dark outlined').classes('w-full').on('keydown.enter', lambda: self.procesar_ruta_manual(path_input.value))
                        ui.button(icon='arrow_forward', on_click=lambda: self.procesar_ruta_manual(path_input.value)).props('flat round color=blue')

                # Restore Session Button
                if os.path.exists('config/videos_escaneados.json'):
                   with ui.row().classes('w-full justify-center mt-4'):
                       ui.button('Cargar Última Sesión', on_click=self.load_last_scan, icon='history').props('flat color=green-4')

            # Version footer
            ui.label('versión 1.2.0').classes('absolute bottom-6 text-xs text-gray-600 font-mono')

    def render_scanning_state(self):
        """Estado 2: Progreso del escaneo (Bindeado para actualizaciones fluidas)"""
        with ui.card().classes('w-full max-w-4xl h-[75vh] flex flex-col items-center justify-center glass-card relative'):
            
            # Contenido central centrado
            with ui.column().classes('items-center w-full max-w-lg gap-10 p-12'):
                
                # Progreso Circular Grande - Clean Look
                with ui.element('div').classes('relative flex items-center justify-center mb-4'):
                    ui.circular_progress(
                        value=0, # Initial value
                        size='160px',
                        show_value=False,
                    ).props('color=green-500 track-color=grey-2 thickness=0.08 show-value=false class="text-green-500"').bind_value_from(self, 'progress_value')
                    
                    with ui.column().classes('absolute items-center gap-0'):
                        ui.label().classes('text-4xl font-extrabold text-gray-800 dark:text-white tracking-tight').bind_text_from(self, 'progress_value', lambda v: f'{int(v * 100)}%')
                
                with ui.column().classes('items-center gap-3 w-full'):
                    ui.label('Escaneando videos...').classes('text-2xl font-bold text-gray-900 dark:text-white tracking-tight')
                    
                    with ui.row().classes('items-center gap-2 bg-gray-100 dark:bg-gray-800 px-4 py-2 rounded-lg max-w-md'):
                        ui.icon('folder_open', size='18px').classes('text-gray-400')
                        ui.label().classes('text-sm text-gray-500 font-medium truncate').bind_text_from(self, 'current_folder', lambda f: os.path.basename(f) if f else 'Inicializando...')

                # Barra lineal "Total Progress" with labels
                with ui.column().classes('w-full gap-2 mt-2'):
                    with ui.row().classes('w-full justify-between text-xs font-bold text-gray-400 tracking-wider uppercase'):
                        ui.label('Total Progress')
                        ui.label().bind_text_from(self, 'progress_value', lambda v: f'{int(v * 100)}%')
                    
                    ui.linear_progress(value=0).classes('h-2 rounded-full').props('color=blue-600 track-color=blue-100 dark:track-color=gray-800').bind_value_from(self, 'progress_value')

                # Botones de control
                with ui.row().classes('gap-6 mt-6 w-full justify-center'):
                    self.btn_pause = ui.button('PAUSAR', on_click=self.pausar_reanudar).classes(
                        'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 px-10 py-3 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors font-bold text-sm tracking-wide shadow-sm'
                    ).props('unelevated')
                    
                    ui.button('CANCELAR', on_click=self.cancelar_escaneo).classes(
                        'text-gray-400 hover:text-red-500 px-6 font-bold text-sm tracking-wide'
                    ).props('flat')

            # Footer links
            with ui.row().classes('absolute bottom-6 gap-6 text-xs text-gray-400'):
                ui.link('Privacy Policy')
                ui.link('Terms of Service')
                ui.link('Contact')

    def render_results_state(self):
        """Estado 3: Resultados finales"""
        
        # Layout completo de pantalla ancha
        with ui.column().classes('w-full max-w-[1600px] h-screen p-6 gap-6'):
            
            # 1. Top Bar
            with ui.row().classes('w-full items-center justify-between mb-2'):
                with ui.row().classes('items-center gap-8'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('slow_motion_video', size='28px').classes('text-blue-600')
                        ui.label('Video Scanner').classes('text-xl font-bold text-gray-900')
                    
                    with ui.row().classes('gap-6 text-sm font-medium text-gray-500'):
                        ui.label('Dashboard').classes('text-gray-900 cursor-pointer')
                        ui.label('History').classes('text-gray-500 hover:text-gray-900 cursor-pointer')
                        ui.label('Settings').classes('text-gray-500 hover:text-gray-900 cursor-pointer')
                
                with ui.row().classes('items-center gap-4'):
                    ui.input(placeholder='Filter results...').props('rounded outlined dense dark').classes('w-64 bg-[#1e1e1e]')
                    
                    with ui.row().classes('gap-2'):
                        ui.button('Rescan', on_click=self.iniciar_escaneo, icon='refresh').props('outline color=yellow').tooltip('Escanear esta carpeta nuevamente')
                        ui.button('New Scan', on_click=self.reset_to_initial, icon='add').classes('bg-blue-600 text-white rounded-full px-6 text-sm normal-case font-medium hover:bg-blue-700')
                    
                    ui.avatar('person', color='grey-3', text_color='grey-8').classes('cursor-pointer')

            # 2. Main Header
            with ui.row().classes('w-full items-center justify-between'):
                with ui.column().classes('gap-1'):
                    ui.row().classes('text-sm text-gray-400 gap-2 items-center').style('font-family: monospace').clear() # Breadcrumbs fake
                    ui.html('<span class="text-gray-400">Home</span> <span class="text-gray-300">/</span> <span class="font-medium text-gray-600">Scan Results</span>', sanitize=False)
                    
                    ui.label('Scan Results').classes('text-4xl font-extrabold text-gray-900 tracking-tight')
                    with ui.row().classes('items-center gap-2 mt-1'):
                        ui.icon('check_circle', size='16px').classes('text-green-500')
                        ui.label(f'Completed - Finished scanning local storage in {self.time_elapsed} seconds').classes('text-green-600 font-medium text-sm')
                
                ui.button('Clear Results', on_click=self.reset_to_initial).props('outline flat color=grey').classes('text-gray-500')

            # 3. Content Grid
            with ui.grid().classes('w-full gap-6').style('grid-template-columns: 350px 1fr 250px'):
                
                # Column 1: Overview & Stats
                with ui.column().classes('gap-4'):
                    ui.label('OVERVIEW').classes('text-xs font-bold text-gray-500 tracking-wider mb-2')
                    
                    def stat_card(icon, value, label, color_bg, color_text):
                        with ui.card().classes('w-full p-6 flex flex-row items-center gap-4 glass-card border-none flex-shrink-0'):
                            with ui.element('div').classes(f'{color_bg} p-3 rounded-lg'):
                                ui.icon(icon, size='24px').classes(color_text)
                            with ui.column().classes('gap-0'):
                                ui.label(str(value)).classes('text-2xl font-bold text-gray-200 leading-tight')
                                ui.label(label).classes('text-xs font-medium text-gray-500 uppercase')
                                
                    stat_card('folder', f"{self.scan_stats.get('carpetas_escaneadas', 0):,}", 'Folders Scanned', 'bg-blue-900/30', 'text-blue-400')
                    stat_card('movie', f"{self.scan_stats.get('videos_validos', 0):,}", 'Videos Found', 'bg-purple-900/30', 'text-purple-400')
                    stat_card('storage', formatear_tamano(self.scan_stats.get('tamano_total_mb', 0)), 'Total Storage', 'bg-orange-900/30', 'text-orange-400')
                    
                # Column 2: Table
                with ui.card().classes('w-full glass-card h-full flex flex-col p-0 overflow-hidden border-none'):
                    with ui.row().classes('p-6 items-center justify-between border-b border-gray-700'):
                        ui.label('Detected Media').classes('font-bold text-lg text-gray-200')
                        with ui.row().classes('gap-2'):
                             self.btn_move = ui.button('MOVER / COPIAR', on_click=self.open_move_dialog).props('unelevated dense color=primary icon=drive_file_move').classes('hidden')
                             ui.icon('sort').classes('text-gray-500 cursor-pointer')
                        
                    # Table
                    columns = [
                        {'name': 'nombre', 'label': 'FILENAME', 'field': 'nombre', 'align': 'left'},
                        {'name': 'ruta', 'label': 'PATH', 'field': 'subcarpeta', 'align': 'left'},
                        {'name': 'resolucion', 'label': 'RESOLUTION', 'field': 'resolucion', 'align': 'center'},
                        {'name': 'tamano', 'label': 'SIZE', 'field': 'tamano', 'align': 'right'},
                    ]
                    
                    rows = []
                    # Limit to 100 for display performance
                    for v in self.videos[:100]:  
                        rows.append({
                            'nombre': v.nombre,
                            'subcarpeta': v.subcarpeta[:30] + '...' if len(v.subcarpeta) > 30 else v.subcarpeta,
                            'ruta': v.ruta,
                            'resolucion': v.resolucion,
                            'tamano': formatear_tamano(v.tamano_mb),
                            'full_obj': v # Store full object for actions
                        })

                    # Function to handle selection
                    self.selected_rows = []
                    def on_selection(e):
                        self.selected_rows = e.selection
                        if self.selected_rows:
                            self.btn_move.classes(remove='hidden')
                            self.btn_move.set_text(f'MOVER ({len(self.selected_rows)})')
                        else:
                            self.btn_move.classes(add='hidden')

                    self.table = ui.table(
                        columns=columns, 
                        rows=rows, 
                        row_key='nombre',
                        selection='multiple',
                        on_select=on_selection
                    ).classes('w-full h-full text-gray-300').props('flat dark')

                    with ui.row().classes('p-4 justify-center border-t border-gray-700'):
                         ui.label('Show more entries').classes('text-xs font-semibold text-gray-500 cursor-pointer hover:text-blue-400')

                # Column 3: Actions
                with ui.column().classes('gap-4'):
                     ui.label('ACTIONS').classes('text-xs font-bold text-gray-500 tracking-wider mb-2')
                     
                     with ui.column().classes('w-full gap-3'):
                         def action_btn(label, icon, sub, on_click):
                             with ui.button(on_click=on_click).classes('w-full bg-[#252525] border border-gray-700 hover:border-blue-500 text-left px-4 py-3 rounded-xl shadow-md flex flex-row items-center justify-start gap-4 h-auto group').props('unelevated no-caps'):
                                 with ui.element('div').classes('bg-blue-900/20 p-2 rounded-lg group-hover:bg-blue-900/40 transition-colors'):
                                     ui.icon(icon).classes('text-blue-400')
                                 with ui.column().classes('gap-0 items-start'):
                                     ui.label(label).classes('font-bold text-gray-200 text-sm')
                                     ui.label(sub).classes('text-xs text-gray-500 font-normal')

                         action_btn('JSON', 'data_object', 'Export raw data', self.exportar_json)
                         action_btn('CSV', 'table_view', 'Open for Excel', self.exportar_csv)
                         action_btn('Fix Log', 'bug_report', 'View errors', lambda: os.startfile(os.path.abspath('logs/scanner.log')))
                         
                         ui.button('Download All', on_click=self.exportar_json).classes(
                             'w-full bg-blue-600 text-white font-bold rounded-xl py-3 shadow-lg hover:bg-blue-700 hover:shadow-blue-900 mt-4'
                         )
                         
                     # Quick Tip Card
                     with ui.card().classes('w-full bg-blue-900/20 p-6 mt-4 border border-blue-900/50 shadow-none'):
                         with ui.row().classes('items-center gap-2 mb-2'):
                             ui.icon('lightbulb', size='20px').classes('text-blue-400')
                             ui.label('QUICK TIP').classes('font-bold text-blue-400 text-xs tracking-wider')
                         
                         ui.label("You can filter by resolution (e.g. '4K') directly in the search bar above to isolate specific file qualities.").classes('text-sm text-blue-300 leading-relaxed')

    def open_move_dialog(self):
        """Dialog to move/copy selected files"""
        if not self.selected_rows:
            return

        with ui.dialog() as dialog, ui.card().classes('w-full max-w-lg bg-[#1e1e1e] border border-gray-700'):
            ui.label(f'Gestionar {len(self.selected_rows)} elementos').classes('text-xl font-bold text-white mb-4')
            
            target_folder = {'path': None}
            lbl_path = ui.label('Ninguna carpeta seleccionada').classes('text-sm text-gray-400 break-all bg-black/20 p-2 rounded w-full mb-4')
            
            def on_folder_select(path):
                target_folder['path'] = path
                lbl_path.text = f"Destino: {path}"
                
            def select_dest():
                 # Reuse existing folder picker logic mechanism?
                 # Need to launch a nested dialog or handle stack.
                 # For simplicity, we create a Picker within this scope or separate function.
                 self.launch_picker(on_folder_select)

            ui.button('Seleccionar Destino', on_click=select_dest).props('outline color=blue')

            with ui.row().classes('w-full justify-end gap-2 mt-6'):
                async def execute(action):
                    if not target_folder['path']:
                        ui.notify('Seleccione carpeta destino', type='warning')
                        return
                    dialog.close()
                    await self.execute_file_operation(action, target_folder['path'])

                ui.button('Cancelar', on_click=dialog.close).props('flat color=grey')
                ui.button('Copiar', on_click=lambda: execute('copy')).classes('bg-green-700')
                ui.button('Mover', on_click=lambda: execute('move')).classes('bg-blue-700')

        dialog.open()

    def launch_picker(self, callback):
        """Helper to launch picker for secondary operations"""
        with ui.dialog() as dialog, ui.card().classes('p-0 rounded-xl overflow-hidden'):
            picker = FolderPicker(
                directory=self.carpeta_seleccionada or os.getcwd(),
                on_select=lambda p: (dialog.close(), callback(p)),
                on_cancel=dialog.close
            )
        dialog.open()

    async def execute_file_operation(self, action, base_target_path):
        import shutil
        import re
        
        ui.notify('Iniciando operación inteligente...', type='info')
        
        success_count = 0
        errors = 0
        
        # Helper to count files in a directory
        def get_file_count(path):
            try:
                return len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
            except:
                return 0

        # Determine Context
        # If selected folder is a "leaf" (matches pattern), start there, overflow to siblings.
        # If selected folder is "root" (no pattern), start with last child matching pattern, or create 0001.
        
        target_name = os.path.basename(base_target_path.rstrip(os.sep))
        match = re.match(r'^(\d+)-videos$', target_name)
        
        if match:
            # We are inside a numbered folder
            current_target = base_target_path
            parent_path = os.path.dirname(base_target_path)
            current_num = int(match.group(1))
        else:
            # We are in a parent folder
            parent_path = base_target_path
            # Find latest chunk
            subfolders = []
            if os.path.exists(parent_path):
                for name in os.listdir(parent_path):
                    path = os.path.join(parent_path, name)
                    if os.path.isdir(path):
                        m = re.match(r'^(\d+)-videos$', name)
                        if m:
                            subfolders.append((int(m.group(1)), path))
            subfolders.sort()
            
            if subfolders:
                current_num, current_target = subfolders[-1]
            else:
                current_num = 1
                current_target = os.path.join(parent_path, f"{current_num:04d}-videos")
                os.makedirs(current_target, exist_ok=True)
                self.scanner.logger.info(f"Creada carpeta inicial: {os.path.basename(current_target)}")
        
        # Processing Queue
        queue = list(self.selected_rows)
        
        while queue:
            # Check capacity of current_target
            # (Re-verify existence in case we just defined it string-wise)
            if not os.path.exists(current_target):
                 os.makedirs(current_target, exist_ok=True)
                 
            count = get_file_count(current_target)
            space = 50 - count
            
            if space <= 0:
                # Need new folder
                current_num += 1
                new_folder_name = f"{current_num:04d}-videos"
                current_target = os.path.join(parent_path, new_folder_name)
                os.makedirs(current_target, exist_ok=True)
                self.scanner.logger.info(f"Creada carpeta secuencial: {new_folder_name}")
                space = 50 # New folder is empty
            
            # Take batch
            batch = queue[:space]
            queue = queue[space:]
            
            for row in batch:
                video = row['full_obj']
                
                # Handle dictionary (serialized) vs object
                if isinstance(video, dict):
                    src = video.get('ruta')
                    name = video.get('nombre')
                else:
                    src = video.ruta
                    name = video.nombre
                    
                dst = os.path.join(current_target, name)
                
                # Collision handling
                if os.path.exists(dst):
                    base, ext = os.path.splitext(name)
                    dst = os.path.join(current_target, f"{base}_copy{ext}")

                try:
                    if action == 'move':
                        shutil.move(src, dst)
                    else:
                        shutil.copy2(src, dst)
                    success_count += 1
                except Exception as e:
                    print(f"Error {action} {src}: {e}")
                    errors += 1
        
        ui.notify(f'Operación completada: {success_count} procesados, {errors} errores', type='positive' if errors == 0 else 'warning')
        
        # Cleanup if moved
        if action == 'move':
             # Refresh list logic
             # Helper to safely extract path
             def get_path(obj):
                 if isinstance(obj, dict): return obj.get('ruta')
                 return obj.ruta

             moved_paths = [get_path(r['full_obj']) for r in self.selected_rows]
             self.videos = [v for v in self.videos if v.ruta not in moved_paths]
             self.render_content.refresh()

    def reset_to_initial(self):
        self.state = 'initial'
        self.progress_value = 0
        self.current_folder = ""
        self.render_content.refresh()

    def load_last_scan(self):
        """Cargar resultados previos"""
        p = 'config/videos_escaneados.json'
        if not os.path.exists(p):
            ui.notify('No hay sesión previa guardada', type='warning')
            return
            
        videos, stats, root = self.scanner.cargar_resultados(p)
        if videos:
            self.videos = videos
            self.scan_stats = stats
            self.carpeta_seleccionada = root or "Desconocido"
            self.time_elapsed = 0 # No time info stored for duration of scan, reset or ignore
            
            self.state = 'results'
            self.render_content.refresh()
            ui.notify(f'Sesión cargada: {len(videos)} videos', type='positive')
        else:
             ui.notify('Error al cargar la sesión', type='negative')

    async def seleccionar_carpeta(self):
        """Abrir selector de carpetas integrado en la UI (Funciona en Web y Local)"""
        
        with ui.dialog() as dialog, ui.card().classes('p-0 rounded-xl overflow-hidden'):
            def on_select(path):
                dialog.close()
                self.procesar_ruta_manual(path)
                
            def on_cancel():
                dialog.close()
                
            picker = FolderPicker(
                directory=self.carpeta_seleccionada or os.getcwd(),
                on_select=on_select,
                on_cancel=on_cancel
            )
            
        dialog.open()

    def procesar_ruta_manual(self, ruta: str):
        """Validar e iniciar escaneo desde una ruta dada"""
        if not ruta:
            return
            
        ruta = os.path.abspath(ruta.strip()) # Limpiar y normalizar
        
        if os.path.exists(ruta) and os.path.isdir(ruta):
            self.carpeta_seleccionada = ruta
            ui.notify(f'Seleccionado: {os.path.basename(ruta)}', type='positive')
            # Es necesario programar la tarea async
            asyncio.create_task(self.iniciar_escaneo())
        else:
            ui.notify('La ruta no existe o no es un directorio válido', type='negative')
    
    async def iniciar_escaneo(self):
        """Iniciar proceso de escaneo recursivo"""
        if not self.carpeta_seleccionada:
            return
        
        self.state = 'scanning'
        self.render_content.refresh()
        self.start_time = time.time()
        
        # Callback para actualizar UI (ahora sólo actualiza variables)
        def actualizar_progreso(total, actual, carpeta_actual):
            progreso = (actual / total) if total > 0 else 0
            self.progress_value = progreso
            self.current_folder = carpeta_actual

        try:
            loop = asyncio.get_event_loop()
            
            async def scan_task():
                return await loop.run_in_executor(
                    None,
                    self.scanner.escanear_recursivo,
                    self.carpeta_seleccionada,
                    actualizar_progreso
                )
            
            task = asyncio.create_task(scan_task())
            
            # loop para mantener la UI viva si fuera necesario (NiceGUI usa websockets, debería estar bien)
            # Pero sin este loop await, la función retornaría inmediatamente y el task seguiría en background
            # Queremos esperar a que termine para cambiar a resultados
            await task
            
            self.videos = task.result()
            self.scan_stats = self.scanner.stats
            self.time_elapsed = int(time.time() - self.start_time)
            
            self.state = 'results'
            self.render_content.refresh()
            
            # Auto-save
            self.scanner.guardar_resultados(self.videos, 'config/videos_escaneados.json', self.carpeta_seleccionada)
            
        except Exception as e:
            ui.notify(f'Error: {str(e)}', type='negative')
            self.state = 'initial'
            self.render_content.refresh()

    def pausar_reanudar(self):
        if self.scanner.paused:
            self.scanner.resume()
            self.btn_pause.set_text('PAUSAR')
        else:
            self.scanner.pause()
            self.btn_pause.set_text('REANUDAR')

    def cancelar_escaneo(self):
        self.scanner.cancel()
        self.state = 'initial'
        self.render_content.refresh()

    async def exportar_json(self):
        output = 'config/videos_escaneados.json'
        # Ensure directory exists in case it was deleted
        os.makedirs(os.path.dirname(output), exist_ok=True)
        
        success = self.scanner.guardar_resultados(self.videos, output, self.carpeta_seleccionada)
        if success:
             os.startfile(os.path.abspath(output))
        else:
             ui.notify('Error al guardar JSON', type='negative')

    def exportar_csv(self):
        import csv
        output = 'config/videos_escaneados.csv'
        os.makedirs(os.path.dirname(output), exist_ok=True)
        
        try:
            with open(output, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['Nombre', 'Ruta', 'Duración', 'Tamaño MB', 'Resolución'])
                for v in self.videos:
                    writer.writerow([v.nombre, v.ruta, formatear_duracion(v.duracion_segundos), v.tamano_mb, v.resolucion])
            os.startfile(os.path.abspath(output))
        except Exception as e:
            ui.notify(f'Error CSV: {e}', type='negative')

def main():
    app_instance = VideoScannerApp()
    app_instance.create_ui()
    
    ui.run(
        title='Video Scanner Pro',
        host='localhost',
        port=8081,
        reload=False,
        show=True,
        # dark=False # Forzamos modo claro
    )

if __name__ in {"__main__", "__mp_main__"}:
    main()
