STORAGE NA MinIO!

Inicjalizacja migracji (tylko raz na projekt)
Tworzy folder migrations:
flask db init

Tworzenie nowej migracji
Tworzy plik migracji na podstawie zmian w modelach:
flask db migrate -m "opis zmian"

Zastosowanie migracji w bazie danych
Wykonuje wszystkie migracje w bazie danych:
flask db upgrade

w folderze services/auth
flask run
w folderze services
python3 -m auth.app
