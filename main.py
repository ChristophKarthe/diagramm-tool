"""
Diagramm-Tool: Desktop-Anwendung zum Erstellen von Diagrammen aus Tabellendaten
Verwendet PyQt5 für die GUI und Plotly für interaktive Diagramme
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QComboBox, 
                             QLineEdit, QFileDialog, QMessageBox, QGroupBox,
                             QSizeGrip, QStatusBar)
from PyQt5.QtCore import Qt, QPoint
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import webbrowser
import tempfile
import os
import base64
from title_bar import CustomTitleBar
from ressources import ARROW_ICON_BASE64

class DiagrammTool(QMainWindow):
    def __init__(self):
        super().__init__()
        # Entfernt die Standard-Fensterleiste
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.df = None
        self.init_ui()
    
    def init_ui(self):
        """Initialisiert die Benutzeroberfläche"""
        self.setWindowTitle("Diagramm-Tool")
        self.setGeometry(100, 100, 800, 350) # Höhe angepasst für Titelleiste
        
        # Hauptwidget und Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Globales Layout mit Titelleiste oben
        global_layout = QVBoxLayout(main_widget)
        global_layout.setContentsMargins(0,0,0,0)
        global_layout.setSpacing(0)

        self.title_bar = CustomTitleBar(self)
        global_layout.addWidget(self.title_bar)

        # Inhalts-Container für den Rest der App
        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(10,10,10,10) # Innenabstand für Inhalt
        global_layout.addWidget(content_widget, 1) # Stretch-Faktor hinzugefügt

        # Statusleiste für den SizeGrip
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        size_grip = QSizeGrip(self.status_bar)
        self.status_bar.addPermanentWidget(size_grip)

        # Datei-Laden Bereich
        file_group = QGroupBox("Daten laden")
        file_layout = QHBoxLayout()
        
        self.file_label = QLabel("Keine Datei geladen")
        self.load_btn = QPushButton("Datei öffnen")
        self.load_btn.clicked.connect(self.load_file)
        
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.load_btn)
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)
        
        # Achsen-Konfiguration Bereich
        config_group = QGroupBox("Diagramm-Konfiguration")
        config_layout = QVBoxLayout()
        
        # X-Achse
        x_layout = QHBoxLayout()
        x_layout.addWidget(QLabel("X-Achse:"))
        self.x_combo = QComboBox()
        self.x_combo.setMinimumWidth(200)
        x_layout.addWidget(self.x_combo)
        x_layout.addWidget(QLabel("Beschriftung:"))
        self.x_label_input = QLineEdit()
        self.x_label_input.setPlaceholderText("Optional")
        x_layout.addWidget(self.x_label_input)
        x_layout.addStretch()
        config_layout.addLayout(x_layout)
        
        # Y-Achse
        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel("Y-Achse:"))
        self.y_combo = QComboBox()
        self.y_combo.setMinimumWidth(200)
        y_layout.addWidget(self.y_combo)
        y_layout.addWidget(QLabel("Beschriftung:"))
        self.y_label_input = QLineEdit()
        self.y_label_input.setPlaceholderText("Optional")
        y_layout.addWidget(self.y_label_input)
        y_layout.addStretch()
        config_layout.addLayout(y_layout)
        
        # Diagrammtyp
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Diagrammtyp:"))
        self.chart_type = QComboBox()
        self.chart_type.addItems([
            "Liniendiagramm",
            "Balkendiagramm",
            "Streudiagramm",
            "Flächendiagramm",
            "Balkendiagramm (horizontal)"
        ])
        self.chart_type.setMinimumWidth(200)
        type_layout.addWidget(self.chart_type)
        type_layout.addStretch()
        config_layout.addLayout(type_layout)
        
        # Titel
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Diagrammtitel:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Optional")
        title_layout.addWidget(self.title_input)
        config_layout.addLayout(title_layout)
        
        # Button zum Erstellen
        button_layout = QHBoxLayout()
        self.create_btn = QPushButton("Diagramm erstellen")
        self.create_btn.setEnabled(False)
        self.create_btn.clicked.connect(self.create_diagram)
        button_layout.addStretch()
        button_layout.addWidget(self.create_btn)
        button_layout.addStretch()
        config_layout.addLayout(button_layout)
        
        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)
        
        # Der Bereich für die Diagramm-Anzeige wird entfernt
        
        self.export_btn = QPushButton("Als HTML exportieren")
        self.export_btn.setEnabled(False)
        self.export_btn.clicked.connect(self.export_diagram)
        main_layout.addWidget(self.export_btn)
        
        # Stretch-Faktor ist nicht mehr nötig
        main_layout.addStretch(1)
    
    def load_file(self):
        """Lädt eine Datei (CSV oder Excel) und aktualisiert die Spaltenauswahl"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Datei öffnen",
            "",
            "Tabellendaten (*.csv *.xlsx *.xls);;CSV (*.csv);;Excel (*.xlsx *.xls);;Alle Dateien (*.*)"
        )
        
        if file_path:
            try:
                # Datei laden
                if file_path.endswith('.csv'):
                    self.df = pd.read_csv(file_path)
                elif file_path.endswith(('.xlsx', '.xls')):
                    self.df = pd.read_excel(file_path)
                else:
                    raise ValueError("Nicht unterstütztes Dateiformat")
                
                # UI aktualisieren
                self.file_label.setText(f"Geladen: {file_path.split('/')[-1]}")
                
                # Spalten in die Comboboxen laden
                columns = list(self.df.columns)
                self.x_combo.clear()
                self.y_combo.clear()
                self.x_combo.addItems(columns)
                self.y_combo.addItems(columns)
                
                # Standardwerte setzen
                if len(columns) > 1:
                    self.y_combo.setCurrentIndex(1)
                
                # Button aktivieren
                self.create_btn.setEnabled(True)
                
                QMessageBox.information(
                    self,
                    "Erfolg",
                    f"Datei erfolgreich geladen!\n{len(self.df)} Zeilen, {len(columns)} Spalten"
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Fehler",
                    f"Fehler beim Laden der Datei:\n{str(e)}"
                )
    
    def create_diagram(self):
        """Erstellt das Diagramm basierend auf der Konfiguration"""
        if self.df is None:
            return
        
        try:
            # Konfiguration auslesen
            x_col = self.x_combo.currentText()
            y_col = self.y_combo.currentText()
            x_label = self.x_label_input.text() or x_col
            y_label = self.y_label_input.text() or y_col
            title = self.title_input.text() or f"{y_label} vs {x_label}"
            chart_type = self.chart_type.currentText()
            
            # Diagramm erstellen basierend auf Typ
            if chart_type == "Liniendiagramm":
                fig = px.line(self.df, x=x_col, y=y_col, title=title)
            elif chart_type == "Balkendiagramm":
                fig = px.bar(self.df, x=x_col, y=y_col, title=title)
            elif chart_type == "Streudiagramm":
                fig = px.scatter(self.df, x=x_col, y=y_col, title=title)
            elif chart_type == "Flächendiagramm":
                fig = px.area(self.df, x=x_col, y=y_col, title=title)
            elif chart_type == "Balkendiagramm (horizontal)":
                fig = px.bar(self.df, x=y_col, y=x_col, orientation='h', title=title)
                x_label, y_label = y_label, x_label  # Achsen tauschen
            
            # Achsenbeschriftungen setzen
            fig.update_xaxes(title_text=x_label)
            fig.update_yaxes(title_text=y_label)
            
            # Layout anpassen
            fig.update_layout(
                hovermode='closest',
                template='plotly_white',
                height=600
            )
            
            self.current_fig = fig
            
            # Temporäre HTML-Datei erstellen und im Browser öffnen
            with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as f:
                fig.write_html(f)
                # URL für den Browser erstellen (funktioniert auf allen Systemen)
                file_url = 'file:///' + os.path.abspath(f.name).replace('\\', '/')

            webbrowser.open(file_url)
            
            # Export-Button aktivieren
            self.export_btn.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Fehler beim Erstellen des Diagramms:\n{str(e)}"
            )
    
    def export_diagram(self):
        """Exportiert das aktuelle Diagramm als HTML-Datei"""
        if not hasattr(self, 'current_fig'):
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Diagramm exportieren",
            "diagramm.html",
            "HTML (*.html);;Alle Dateien (*.*)"
        )
        
        if file_path:
            try:
                self.current_fig.write_html(file_path)
                QMessageBox.information(
                    self,
                    "Erfolg",
                    f"Diagramm erfolgreich exportiert:\n{file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Fehler",
                    f"Fehler beim Exportieren:\n{str(e)}"
                )


def main():
    app = QApplication(sys.argv)

    # Base64-kodierter Pfeil für das Dropdown-Menü
    arrow_png_data = base64.b64decode(ARROW_ICON_BASE64)

    with open("arrow.png", "wb") as f:
        f.write(arrow_png_data)

    # Stylesheet aus externer Datei laden
    try:
        with open("styles.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Stylesheet-Datei 'styles.qss' nicht gefunden.")
    
    window = DiagrammTool()
    window.show()
    
    exit_code = app.exec_()
    
    # Temporäre Pfeil-Datei löschen
    if os.path.exists("arrow.png"):
        os.remove("arrow.png")
        
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
