#!/usr/bin/env python
"""
Script to help identify templates that need internationalization.
This script searches for common German words in HTML templates.
"""
import re
from pathlib import Path

# Common German words/phrases that should be translated
GERMAN_PATTERNS = [
    r'\bSchüler\b',
    r'\bVertrag\b',
    r'\bStunde\b',
    r'\bBlockzeit\b',
    r'\bBearbeiten\b',
    r'\bLöschen\b',
    r'\bErstellen\b',
    r'\bDetails\b',
    r'\bHinweis\b',
    r'\bFehler\b',
    r'\bErfolg\b',
    r'\bWarnung\b',
    r'\bSpeichern\b',
    r'\bAbbrechen\b',
    r'\bZurück\b',
    r'\bNeuer\b',
    r'\bNeue\b',
    r'\bAktiv\b',
    r'\bInaktiv\b',
    r'\bunbefristet\b',
    r'\bMin\.\b',
    r'\bUhr\b',
    r'\bDatum\b',
    r'\bZeit\b',
    r'\bStatus\b',
    r'\bAktionen\b',
    r'\bKonflikte\b',
    r'\bGeplant\b',
    r'\bUnterrichtet\b',
    r'\bAusgezahlt\b',
    r'\bAusgefallen\b',
    r'\bFahrtzeiten\b',
    r'\bVorher\b',
    r'\bNachher\b',
    r'\bNotizen\b',
    r'\bKollidierende\b',
    r'\bVertragskontingent\b',
    r'\büberschritten\b',
    r'\bEinheiten\b',
    r'\bTatsächlich\b',
    r'\bGeplant\b',
    r'\bStunden\b',
    r'\bHinweis\b',
    r'\bNachholen\b',
    r'\bVorarbeiten\b',
]

def find_german_text_in_template(template_path):
    """Find German text in a template file."""
    try:
        content = template_path.read_text(encoding='utf-8')
        matches = []
        for pattern in GERMAN_PATTERNS:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                # Skip if already in {% trans %} or {% blocktrans %}
                context_start = max(0, match.start() - 50)
                context_end = min(len(content), match.end() + 50)
                context = content[context_start:context_end]
                if '{% trans' not in context and '{% blocktrans' not in context:
                    matches.append((match.group(), match.start(), match.end()))
        return matches
    except Exception as e:
        print(f"Error reading {template_path}: {e}")
        return []

def main():
    """Main function."""
    backend_dir = Path(__file__).parent.parent
    templates_dir = backend_dir / 'apps'
    
    templates_with_german = []
    
    for template_file in templates_dir.rglob('*.html'):
        matches = find_german_text_in_template(template_file)
        if matches:
            templates_with_german.append((template_file, matches))
    
    print(f"Found {len(templates_with_german)} templates with potential German text:")
    for template_path, matches in templates_with_german:
        print(f"\n{template_path.relative_to(backend_dir)}")
        print(f"  {len(matches)} potential matches")

if __name__ == '__main__':
    main()

