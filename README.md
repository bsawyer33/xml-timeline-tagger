# XML Timeline Tagger & Organizer

A command-line script for macOS that cross-references a Premiere Pro/FCP XML with a master footage folder. It automatically isolates unused media, mirrors the exact folder directory structure, and tags the moved assets in Red.

## One-Step Installation

Open your Mac Terminal, copy the code block below, paste it, and hit **Enter**:

```bash
mkdir -p ~/Developer && curl -sL "[https://raw.githubusercontent.com/bsawyer33/xml-timeline-tagger/main/tagger.py](https://raw.githubusercontent.com/bsawyer33/xml-timeline-tagger/main/tagger.py)" -o ~/Developer/tagger.py && touch ~/.zshrc && sed -i '' '/alias timelinetagger=/d' ~/.zshrc 2>/dev/null || true && echo "alias timelinetagger='python3 ~/Developer/tagger.py'" >> ~/.zshrc && alias timelinetagger='python3 ~/Developer/tagger.py' && echo "\n🎉 Setup complete! Type 'timelinetagger' to run it."
