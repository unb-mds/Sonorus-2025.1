gnome-terminal -- bash -c "cd ~/projetos/Sonorus-2025.1; source ~/Venvs/SonorusVenv/bin/activate; uvicorn src.backend.main:app --reload; exec bash"

gnome-terminal -- bash -c "cd ~/projetos/Sonorus-2025.1/src/frontend; npm start; exec bash"