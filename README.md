---
title: Readme 
author: BongoKnight 
...

# Editeur de texte pour pandoc

## Sources


L'éditeur utilisé comme base provient de GitHub : [https://github.com/goldsborough/Writer-Tutorial](https://github.com/goldsborough/Writer-Tutorial).

Le formattage de la coloration syntaxique provient de : [https://github.com/rupeshk/MarkdownHighlighter/blob/master/markdownhighlighter.py](https://github.com/rupeshk/MarkdownHighlighter/blob/master/markdownhighlighter.py)

## Objectif

Ecrire des notes dans un format simple, les exporter facilement dans différents formats sans avoir à lever les mains du clavier.

## Remarques

Lors de l'insertion d'une image, le chemin absolu est renseigné. Pour l'export en PDF ou en docx celà ne pose pas de problèmes. En revanche, dans le cas d'un export en HTML l'envoi du document résultant n'incluera pas les images.

Cet éditeur se sert de pypandoc pour exploiter les fonctionnalités de pandoc. Pypandoc demande que pandoc soit installé sur la machine.

De la même manière pour pouvoir générer des PDF, pandoc a besoin d'une installation de Latex.

## Améliorations envisagées

- [x] Export dans différents formats : HTML, PDF, Tex, docx
- [ ] Export avec possibilité de définir un template
- [ ] Réouverture du dernier fichier ouvert ( => fichier de config)
- [ ] Possibilité de choisir un fichier CSS, inclure par défaut du  CSS comme GitHub pour l'export HTML.
- [ ] Faire un exécutable avec PyInstaller
- [ ] Refactoring pour réduire la taille de la classe TextEdit
- [ ] Modifier légérement les couleurs de la coloration syntaxique
- [ ] Plusieurs onglets d'éditions
- [ ] Prévisualisation dans une WebView
- [ ] Correction orthographique
- [ ] Sélection d'arguments lors de l'export : --standalone-file, --toc ...
