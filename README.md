# Diagramm-Tool

Eine Desktop-Anwendung zum Erstellen interaktiver Diagramme aus Tabellendaten mit PyQt5 und Plotly.

## Features

- **Interaktive Diagramme** mit Plotly
- **Unterstützt CSV und Excel** (.csv, .xlsx, .xls)
- **Verschiedene Diagrammtypen**:
  - Liniendiagramm
  - Balkendiagramm
  - Streudiagramm
  - Flächendiagramm
  - Horizontale Balkendiagramme
- **Freie Achsenwahl** und Beschriftung
- **HTML-Export** für Diagramme
- **Moderne GUI** mit PyQt5

## Installation

### Voraussetzungen

- Python 3.8 oder höher
- pip (Python Package Installer)

### Schritt 1: Repository klonen oder herunterladen

```bash
git clone https://github.com/ChristophKarthe/diagramm-tool.git
cd diagramm-tool
```

### Schritt 2: Virtuelle Umgebung erstellen (empfohlen)

```bash
python -m venv venv
```

### Schritt 3: Virtuelle Umgebung aktivieren

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.\venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Schritt 4: Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

## Verwendung

### Anwendung starten

```bash
python main.py
```

### mit .exe
- oder einfach die .exe in /dist herunterladen und ausführen

### Arbeitsablauf

1. **Datei laden**: Klicken Sie auf "Datei öffnen" und wählen Sie eine CSV- oder Excel-Datei
2. **Achsen wählen**: Wählen Sie aus den Dropdown-Menüs die Spalten für X- und Y-Achse
3. **Beschriftungen anpassen**: (Optional) Geben Sie eigene Achsenbeschriftungen ein
4. **Diagrammtyp wählen**: Wählen Sie den gewünschten Diagrammtyp
5. **Titel setzen**: (Optional) Geben Sie einen Diagrammtitel ein
6. **Diagramm erstellen**: Klicken Sie auf "Diagramm erstellen"
7. **Exportieren**: (Optional) Exportieren Sie das Diagramm als HTML-Datei

### Testdaten

Eine Beispiel-CSV-Datei (`beispiel_daten.csv`) ist im Repository enthalten.

## Technologie-Stack

- **PyQt5**: GUI-Framework für die Desktop-Anwendung
- **PyQtWebEngine**: Einbettung von HTML-Inhalten (für Plotly)
- **Plotly**: Interaktive Diagramm-Bibliothek
- **Pandas**: Datenverarbeitung und -analyse
- **openpyxl**: Excel-Datei-Unterstützung

## Erweiterungsmöglichkeiten

- mehrere Graphen in ein Diagramm

## Lizenz

Siehe [LICENSE](LICENSE) Datei.

## Autor

Christoph Karthe
