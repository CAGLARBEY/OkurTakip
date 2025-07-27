import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter
from PIL import Image, ImageTk
import os

class ReadingTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Okur Takip")
        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)
        
        # Tema seçenekleri
        self.themes = {
            "Modern Açık": {
                "bg": "#ffffff",
                "fg": "#333333",
                "accent": "#4a6fa5",
                "tree_bg": "#ffffff",
                "tree_fg": "#333333",
                "tree_select": "#4a6fa5",
                "header_font": ("Segoe UI", 12, "bold"),
                "text_font": ("Segoe UI", 10),
                "button_bg": "#4a6fa5",
                "button_fg": "#ffffff"
            },
            "Modern Koyu": {
                "bg": "#1e1e1e",
                "fg": "#e0e0e0",
                "accent": "#569cd6",
                "tree_bg": "#252525",
                "tree_fg": "#e0e0e0",
                "tree_select": "#569cd6",
                "header_font": ("Segoe UI", 12, "bold"),
                "text_font": ("Segoe UI", 10),
                "button_bg": "#569cd6",
                "button_fg": "#ffffff"
            },
            "Material Light": {
                "bg": "#f5f5f5",
                "fg": "#212121",
                "accent": "#3f51b5",
                "tree_bg": "#ffffff",
                "tree_fg": "#212121",
                "tree_select": "#3f51b5",
                "header_font": ("Roboto", 12, "bold"),
                "text_font": ("Roboto", 10),
                "button_bg": "#3f51b5",
                "button_fg": "#ffffff"
            },
            "Material Dark": {
                "bg": "#121212",
                "fg": "#e0e0e0",
                "accent": "#bb86fc",
                "tree_bg": "#1e1e1e",
                "tree_fg": "#e0e0e0",
                "tree_select": "#bb86fc",
                "header_font": ("Roboto", 12, "bold"),
                "text_font": ("Roboto", 10),
                "button_bg": "#bb86fc",
                "button_fg": "#000000"
            },
            "Solarized Light": {
                "bg": "#fdf6e3",
                "fg": "#586e75",
                "accent": "#268bd2",
                "tree_bg": "#eee8d5",
                "tree_fg": "#586e75",
                "tree_select": "#268bd2",
                "header_font": ("Segoe UI", 12, "bold"),
                "text_font": ("Segoe UI", 10),
                "button_bg": "#268bd2",
                "button_fg": "#fdf6e3"
            },
            "Solarized Dark": {
                "bg": "#002b36",
                "fg": "#839496",
                "accent": "#b58900",
                "tree_bg": "#073642",
                "tree_fg": "#839496",
                "tree_select": "#b58900",
                "header_font": ("Segoe UI", 12, "bold"),
                "text_font": ("Segoe UI", 10),
                "button_bg": "#b58900",
                "button_fg": "#002b36"
            },
            "Dracula": {
                "bg": "#282a36",
                "fg": "#f8f8f2",
                "accent": "#bd93f9",
                "tree_bg": "#44475a",
                "tree_fg": "#f8f8f2",
                "tree_select": "#bd93f9",
                "header_font": ("Segoe UI", 12, "bold"),
                "text_font": ("Segoe UI", 10),
                "button_bg": "#bd93f9",
                "button_fg": "#282a36"
            },
            "Nord": {
                "bg": "#2e3440",
                "fg": "#d8dee9",
                "accent": "#5e81ac",
                "tree_bg": "#3b4252",
                "tree_fg": "#d8dee9",
                "tree_select": "#5e81ac",
                "header_font": ("Segoe UI", 12, "bold"),
                "text_font": ("Segoe UI", 10),
                "button_bg": "#5e81ac",
                "button_fg": "#d8dee9"
            },
            "Gruvbox": {
                "bg": "#fbf1c7",
                "fg": "#3c3836",
                "accent": "#d65d0e",
                "tree_bg": "#ebdbb2",
                "tree_fg": "#3c3836",
                "tree_select": "#d65d0e",
                "header_font": ("Segoe UI", 12, "bold"),
                "text_font": ("Segoe UI", 10),
                "button_bg": "#d65d0e",
                "button_fg": "#fbf1c7"
            },
            "One Dark": {
                "bg": "#282c34",
                "fg": "#abb2bf",
                "accent": "#e06c75",
                "tree_bg": "#3e4451",
                "tree_fg": "#abb2bf",
                "tree_select": "#e06c75",
                "header_font": ("Segoe UI", 12, "bold"),
                "text_font": ("Segoe UI", 10),
                "button_bg": "#e06c75",
                "button_fg": "#282c34"
            }
        }
        
        # Varsayılan tema
        self.current_theme = "Modern Açık"
        
        # Veritabanı bağlantısı
        self.db_name = "reading_tracker.db"
        self._initialize_database()
        
        # Ana çerçeveler
        self._create_main_frames()
        
        # Widget'ları oluştur
        self._create_widgets()
        
        # Tema sekmesini ekle
        self._create_theme_tab()
        
        # Varsayılan temayı uygula
        self.apply_theme(self.current_theme)
        
        # Verileri yükle
        self.load_books()
        self.load_articles()
        self.update_stats()
        
        # Başlangıçta kitap sekmesini göster
        self.show_books_tab()

    def _create_main_frames(self):
        """Ana çerçeveleri oluştur"""
        # Header frame
        self.header_frame = ttk.Frame(self.root)
        self.header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Content frame
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Stats frame
        self.stats_frame = ttk.Frame(self.root)
        self.stats_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab frames
        self.books_frame = ttk.Frame(self.notebook)
        self.articles_frame = ttk.Frame(self.notebook)
        self.theme_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.books_frame, text="Kitaplar")
        self.notebook.add(self.articles_frame, text="Makaleler")
        self.notebook.add(self.theme_frame, text="Tema")

    def _create_theme_tab(self):
        """Tema seçimi sekmesini oluştur"""
        theme_frame = ttk.Frame(self.theme_frame)
        theme_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(theme_frame, text="Tema Seçin:", font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        # Tema seçenekleri için butonlar
        btn_frame = ttk.Frame(theme_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        themes = list(self.themes.keys())
        
        # İlk 5 tema
        frame1 = ttk.Frame(btn_frame)
        frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        for theme in themes[:5]:
            ttk.Button(
                frame1, text=theme,
                command=lambda t=theme: self.apply_theme(t),
                style="Accent.TButton"
            ).pack(fill=tk.X, padx=5, pady=5)
        
        # Son 5 tema
        frame2 = ttk.Frame(btn_frame)
        frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        for theme in themes[5:]:
            ttk.Button(
                frame2, text=theme,
                command=lambda t=theme: self.apply_theme(t),
                style="Accent.TButton"
            ).pack(fill=tk.X, padx=5, pady=5)
        
        # Önizleme alanı
        preview_frame = ttk.Frame(theme_frame)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(preview_frame, text="Tema Önizleme:", font=("Segoe UI", 11)).pack(anchor=tk.W)
        
        self.preview_canvas = tk.Canvas(preview_frame, height=150, highlightthickness=0)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Önizleme elemanları
        self.preview_header = self.preview_canvas.create_rectangle(0, 0, 800, 40, fill="#ffffff", outline="")
        self.preview_text = self.preview_canvas.create_text(10, 20, anchor=tk.W, text="Başlık", fill="#333333", font=("Segoe UI", 12, "bold"))
        self.preview_button = self.preview_canvas.create_rectangle(650, 10, 750, 30, fill="#4a6fa5", outline="")
        self.preview_button_text = self.preview_canvas.create_text(700, 20, text="Buton", fill="white", font=("Segoe UI", 10))
        
        self.preview_tree = self.preview_canvas.create_rectangle(10, 50, 790, 140, fill="#ffffff", outline="gray")
        self.preview_tree_text1 = self.preview_canvas.create_text(20, 70, anchor=tk.W, text="Satır 1", fill="#333333", font=("Segoe UI", 10))
        self.preview_tree_text2 = self.preview_canvas.create_text(20, 90, anchor=tk.W, text="Satır 2", fill="#333333", font=("Segoe UI", 10))
        self.preview_tree_sel = self.preview_canvas.create_rectangle(10, 110, 790, 130, fill="#4a6fa5", outline="")
        self.preview_tree_sel_text = self.preview_canvas.create_text(20, 120, anchor=tk.W, text="Seçili Satır", fill="white", font=("Segoe UI", 10))

    def apply_theme(self, theme_name):
        """Seçilen temayı uygular"""
        if theme_name not in self.themes:
            return
            
        self.current_theme = theme_name
        theme = self.themes[theme_name]
        
        # Ana arka plan rengi
        self.root.config(bg=theme["bg"])
        
        # Stilleri güncelle
        style = ttk.Style()
        style.theme_use("clam")
        
        # Genel stiller
        style.configure(".", 
                       background=theme["bg"], 
                       foreground=theme["fg"],
                       font=theme["text_font"])
        
        style.configure("TFrame", background=theme["bg"])
        style.configure("TLabel", 
                       background=theme["bg"], 
                       foreground=theme["fg"],
                       font=theme["text_font"])
        
        style.configure("Header.TLabel", 
                       font=theme["header_font"])
        
        style.configure("TButton", 
                       background=theme["button_bg"],
                       foreground=theme["button_fg"],
                       font=theme["text_font"], 
                       padding=5)
        
        style.configure("Accent.TButton", 
                       background=theme["accent"], 
                       foreground=theme["button_fg"])
        
        style.configure("TNotebook", background=theme["bg"])
        style.configure("TNotebook.Tab", 
                       background=theme["bg"], 
                       foreground=theme["fg"], 
                       font=theme["header_font"], 
                       padding=[10, 5])
        
        # Treeview stilleri
        style.configure("Treeview", 
                       background=theme["tree_bg"],
                       foreground=theme["tree_fg"],
                       fieldbackground=theme["tree_bg"],
                       rowheight=25,
                       font=theme["text_font"])
        
        style.configure("Treeview.Heading", 
                       background=theme["accent"],
                       foreground="white",
                       font=theme["header_font"])
        
        style.map("Treeview", 
                 background=[("selected", theme["tree_select"])],
                 foreground=[("selected", "white")])
        
        # Önizlemeyi güncelle
        self.update_preview(theme)
        
        # Tüm widget'ları yenile
        self.refresh_widgets()

    def update_preview(self, theme):
        """Tema önizlemesini günceller"""
        self.preview_canvas.itemconfig(self.preview_header, fill=theme["bg"])
        self.preview_canvas.itemconfig(self.preview_text, fill=theme["fg"], font=theme["header_font"])
        self.preview_canvas.itemconfig(self.preview_button, fill=theme["button_bg"])
        self.preview_canvas.itemconfig(self.preview_button_text, fill=theme["button_fg"], font=theme["text_font"])
        
        self.preview_canvas.itemconfig(self.preview_tree, fill=theme["tree_bg"])
        self.preview_canvas.itemconfig(self.preview_tree_text1, fill=theme["tree_fg"], font=theme["text_font"])
        self.preview_canvas.itemconfig(self.preview_tree_text2, fill=theme["tree_fg"], font=theme["text_font"])
        self.preview_canvas.itemconfig(self.preview_tree_sel, fill=theme["tree_select"])
        self.preview_canvas.itemconfig(self.preview_tree_sel_text, fill="white", font=theme["text_font"])

    def refresh_widgets(self):
        """Tüm widget'ları tema değişikliği için yeniler"""
        # Notebook sekme renklerini güncelle
        for tab in [self.books_frame, self.articles_frame, self.theme_frame]:
            tab_id = self.notebook.index(tab)
            self.notebook.tab(tab_id, text=self.notebook.tab(tab_id, "text"))
        
        # Treeview'ları yeniden yükle
        self.load_books()
        self.load_articles()

    def _create_widgets(self):
        """Tüm widget'ları oluştur"""
        self._create_header_widgets()
        self._create_books_tab()
        self._create_articles_tab()
        self._create_stats_widgets()

    def _create_header_widgets(self):
        """Başlık çerçevesi widget'ları"""
        # Logo
        try:
            img = Image.open("book_icon.png") if os.path.exists("book_icon.png") else None
            if img:
                img = img.resize((40, 40), Image.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                logo_label = ttk.Label(self.header_frame, image=self.logo_img)
                logo_label.grid(row=0, column=0, padx=(0, 10))
        except Exception as e:
            print(f"Logo yüklenirken hata: {e}")

        # Başlık
        title_label = ttk.Label(
            self.header_frame, 
            text="Kitap ve Makale Takip Uygulaması", 
            style="Header.TLabel"
        )
        title_label.grid(row=0, column=1, sticky=tk.W)
        
        # Filtreleme butonları
        btn_frame = ttk.Frame(self.header_frame)
        btn_frame.grid(row=0, column=2, sticky=tk.E, padx=(20, 0))
        
        self.book_filter = tk.StringVar(value="all")
        ttk.Radiobutton(
            btn_frame, text="Tümü", variable=self.book_filter, value="all",
            command=self.load_books
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            btn_frame, text="Okuyor", variable=self.book_filter, value="reading",
            command=self.load_books
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            btn_frame, text="Bitirdi", variable=self.book_filter, value="completed",
            command=self.load_books
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            btn_frame, text="Okunacak", variable=self.book_filter, value="unread",
            command=self.load_books
        ).pack(side=tk.LEFT, padx=5)

    def _create_books_tab(self):
        """Kitaplar sekmesi widget'ları"""
        # Treeview ve scrollbar
        tree_frame = ttk.Frame(self.books_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.books_tree = ttk.Treeview(
            tree_frame, 
            columns=("id", "title", "author", "progress", "status"), 
            show="headings",
            selectmode="browse"
        )
        
        # Sütunlar
        self.books_tree.heading("id", text="ID")
        self.books_tree.heading("title", text="Kitap Adı")
        self.books_tree.heading("author", text="Yazar")
        self.books_tree.heading("progress", text="İlerleme")
        self.books_tree.heading("status", text="Durum")
        
        # Sütun genişlikleri
        self.books_tree.column("id", width=50, anchor=tk.CENTER)
        self.books_tree.column("title", width=250)
        self.books_tree.column("author", width=200)
        self.books_tree.column("progress", width=100, anchor=tk.CENTER)
        self.books_tree.column("status", width=100, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.books_tree.yview)
        self.books_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.books_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Butonlar
        btn_frame = ttk.Frame(self.books_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            btn_frame, text="Yeni Kitap Ekle", 
            command=self.add_book_dialog, style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, text="Düzenle", 
            command=self.edit_book_dialog
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, text="Sil", 
            command=self.delete_book
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, text="İlerleme Kaydet", 
            command=self.record_progress_dialog
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, text="Detaylar", 
            command=self.show_book_details
        ).pack(side=tk.LEFT, padx=5)
        
        # Çift tıklama olayı
        self.books_tree.bind("<Double-1>", lambda e: self.show_book_details())

    def _create_articles_tab(self):
        """Makaleler sekmesi widget'ları"""
        # Treeview ve scrollbar
        tree_frame = ttk.Frame(self.articles_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.articles_tree = ttk.Treeview(
            tree_frame, 
            columns=("id", "title", "author", "source", "status"), 
            show="headings",
            selectmode="browse"
        )
        
        # Sütunlar
        self.articles_tree.heading("id", text="ID")
        self.articles_tree.heading("title", text="Makale Adı")
        self.articles_tree.heading("author", text="Yazar")
        self.articles_tree.heading("source", text="Kaynak")
        self.articles_tree.heading("status", text="Durum")
        
        # Sütun genişlikleri
        self.articles_tree.column("id", width=50, anchor=tk.CENTER)
        self.articles_tree.column("title", width=300)
        self.articles_tree.column("author", width=200)
        self.articles_tree.column("source", width=200)
        self.articles_tree.column("status", width=100, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.articles_tree.yview)
        self.articles_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.articles_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Butonlar
        btn_frame = ttk.Frame(self.articles_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            btn_frame, text="Yeni Makale Ekle", 
            command=self.add_article_dialog, style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, text="Düzenle", 
            command=self.edit_article_dialog
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, text="Sil", 
            command=self.delete_article
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, text="Okundu İşaretle", 
            command=self.mark_article_as_read
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, text="Detaylar", 
            command=self.show_article_details
        ).pack(side=tk.LEFT, padx=5)
        
        # Çift tıklama olayı
        self.articles_tree.bind("<Double-1>", lambda e: self.show_article_details())

    def _create_stats_widgets(self):
        """İstatistik widget'ları"""
        # Grafik çerçevesi
        self.graph_frame = ttk.Frame(self.stats_frame)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)
        
        # Hızlı istatistikler
        stats_btn_frame = ttk.Frame(self.stats_frame)
        stats_btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(
            stats_btn_frame, text="7 Günlük Aktivite", 
            command=lambda: self.plot_reading_activity(7)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            stats_btn_frame, text="30 Günlük Aktivite", 
            command=lambda: self.plot_reading_activity(30)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            stats_btn_frame, text="90 Günlük Aktivite", 
            command=lambda: self.plot_reading_activity(90)
        ).pack(side=tk.LEFT, padx=5)
        
        # Hızlı istatistikler
        quick_stats_frame = ttk.Frame(self.stats_frame)
        quick_stats_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.current_books_label = ttk.Label(quick_stats_frame, text="Okuyor: 0")
        self.current_books_label.pack(side=tk.LEFT, padx=10)
        
        self.completed_books_label = ttk.Label(quick_stats_frame, text="Bitirdi: 0")
        self.completed_books_label.pack(side=tk.LEFT, padx=10)
        
        self.unread_books_label = ttk.Label(quick_stats_frame, text="Okunacak: 0")
        self.unread_books_label.pack(side=tk.LEFT, padx=10)
        
        self.read_articles_label = ttk.Label(quick_stats_frame, text="Okunan Makaleler: 0")
        self.read_articles_label.pack(side=tk.LEFT, padx=10)
        
        self.unread_articles_label = ttk.Label(quick_stats_frame, text="Okunacak Makaleler: 0")
        self.unread_articles_label.pack(side=tk.LEFT, padx=10)

    def _initialize_database(self):
        """Veritabanı tablolarını oluşturur"""
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            
            # Kitaplar tablosu
            c.execute('''CREATE TABLE IF NOT EXISTS books
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         title TEXT NOT NULL,
                         author TEXT,
                         total_pages INTEGER,
                         current_page INTEGER DEFAULT 0,
                         start_date TEXT,
                         end_date TEXT,
                         is_currently_reading INTEGER DEFAULT 0,
                         rating INTEGER,
                         notes TEXT,
                         added_date TEXT DEFAULT CURRENT_TIMESTAMP)''')
            
            # Makaleler tablosu
            c.execute('''CREATE TABLE IF NOT EXISTS articles
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         title TEXT NOT NULL,
                         author TEXT,
                         source TEXT,
                         url TEXT,
                         read_date TEXT,
                         is_read INTEGER DEFAULT 0,
                         rating INTEGER,
                         notes TEXT,
                         added_date TEXT DEFAULT CURRENT_TIMESTAMP)''')
            
            # Okuma kayıtları tablosu
            c.execute('''CREATE TABLE IF NOT EXISTS reading_sessions
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         book_id INTEGER NOT NULL,
                         date TEXT NOT NULL,
                         pages_read INTEGER NOT NULL,
                         minutes_spent INTEGER,
                         FOREIGN KEY(book_id) REFERENCES books(id) ON DELETE CASCADE)''')
            
            # Makale okuma kayıtları
            c.execute('''CREATE TABLE IF NOT EXISTS article_reading_sessions
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         article_id INTEGER NOT NULL,
                         date TEXT NOT NULL,
                         minutes_spent INTEGER NOT NULL,
                         FOREIGN KEY(article_id) REFERENCES articles(id) ON DELETE CASCADE)''')
            
            conn.commit()

    # Kitap işlemleri
    def load_books(self):
        """Kitapları veritabanından yükler ve treeview'da gösterir"""
        filter_by = self.book_filter.get()
        
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            
            if filter_by == 'completed':
                c.execute('''SELECT id, title, author, current_page, total_pages, 
                            ROUND((current_page * 100.0 / total_pages), 1) as progress
                            FROM books WHERE is_currently_reading=0 AND end_date IS NOT NULL
                            ORDER BY end_date DESC''')
            elif filter_by == 'unread':
                c.execute('''SELECT id, title, author, current_page, total_pages, 
                            ROUND((current_page * 100.0 / total_pages), 1) as progress
                            FROM books WHERE is_currently_reading=0 AND start_date IS NULL
                            ORDER BY added_date DESC''')
            elif filter_by == 'reading':
                c.execute('''SELECT id, title, author, current_page, total_pages, 
                            ROUND((current_page * 100.0 / total_pages), 1) as progress
                            FROM books WHERE is_currently_reading=1
                            ORDER BY start_date DESC''')
            else:
                c.execute('''SELECT id, title, author, current_page, total_pages, is_currently_reading,
                            CASE 
                                WHEN is_currently_reading=1 THEN 'Okuyor'
                                WHEN end_date IS NOT NULL THEN 'Bitirdi'
                                WHEN start_date IS NULL THEN 'Okunacak'
                                ELSE 'Duraklatıldı'
                            END as status,
                            ROUND((current_page * 100.0 / total_pages), 1) as progress
                            FROM books
                            ORDER BY 
                                CASE status
                                    WHEN 'Okuyor' THEN 1
                                    WHEN 'Duraklatıldı' THEN 2
                                    WHEN 'Okunacak' THEN 3
                                    ELSE 4
                                END, added_date DESC''')
            
            books = c.fetchall()
        
        # Treeview'ı temizle
        self.books_tree.delete(*self.books_tree.get_children())
        
        # Yeni verileri ekle
        for book in books:
            status = book[6] if len(book) > 6 else ''
            progress = f"{book[5]}%" if len(book) > 5 else '0%'
            
            self.books_tree.insert("", tk.END, values=(
                book[0], book[1], book[2], progress, status
            ))

    def add_book_dialog(self):
        """Yeni kitap ekleme dialog penceresi"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Yeni Kitap Ekle")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Widget'lar
        ttk.Label(dialog, text="Kitap Adı:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Yazar:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        author_entry = ttk.Entry(dialog, width=40)
        author_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Toplam Sayfa:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        pages_entry = ttk.Entry(dialog, width=40)
        pages_entry.grid(row=2, column=1, padx=5, pady=5)
        
        start_reading = tk.BooleanVar()
        ttk.Checkbutton(
            dialog, text="Hemen okumaya başla", 
            variable=start_reading
        ).grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Butonlar
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            btn_frame, text="İptal", 
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, text="Kaydet", style="Accent.TButton",
            command=lambda: self.save_new_book(
                title_entry.get(),
                author_entry.get(),
                pages_entry.get(),
                start_reading.get(),
                dialog
            )
        ).pack(side=tk.LEFT, padx=5)
        
        # Odaklanma
        title_entry.focus_set()

    def save_new_book(self, title, author, pages, start_reading, dialog):
        """Yeni kitabı veritabanına kaydeder"""
        if not title:
            messagebox.showerror("Hata", "Kitap adı boş olamaz!")
            return
            
        try:
            total_pages = int(pages) if pages else None
        except ValueError:
            messagebox.showerror("Hata", "Sayfa sayısı geçerli bir sayı olmalıdır!")
            return
            
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute('''INSERT INTO books (title, author, total_pages, start_date, is_currently_reading)
                         VALUES (?, ?, ?, ?, ?)''',
                         (title, author, total_pages, current_date if start_reading else None, 
                          1 if start_reading else 0))
            conn.commit()
            
        dialog.destroy()
        self.load_books()
        self.update_stats()
        messagebox.showinfo("Başarılı", "Kitap başarıyla eklendi!")

    def edit_book_dialog(self):
        """Kitap düzenleme dialog penceresi"""
        selected = self.books_tree.focus()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen düzenlemek için bir kitap seçin!")
            return
            
        book_id = self.books_tree.item(selected)['values'][0]
        book = self.get_book_details(book_id)
        
        if not book:
            messagebox.showerror("Hata", "Kitap bilgileri alınamadı!")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("Kitap Düzenle")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Widget'lar
        ttk.Label(dialog, text="Kitap Adı:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.insert(0, book[1])
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Yazar:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        author_entry = ttk.Entry(dialog, width=40)
        author_entry.insert(0, book[2] if book[2] else "")
        author_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Toplam Sayfa:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        pages_entry = ttk.Entry(dialog, width=40)
        pages_entry.insert(0, book[3] if book[3] else "")
        pages_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Mevcut Sayfa:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        current_page_entry = ttk.Entry(dialog, width=40)
        current_page_entry.insert(0, book[4] if book[4] else "0")
        current_page_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Butonlar
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            btn_frame, text="İptal", 
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, text="Kaydet", style="Accent.TButton",
            command=lambda: self.update_book(
                book_id,
                title_entry.get(),
                author_entry.get(),
                pages_entry.get(),
                current_page_entry.get(),
                dialog
            )
        ).pack(side=tk.LEFT, padx=5)
        
        # Odaklanma
        title_entry.focus_set()

    def update_book(self, book_id, title, author, total_pages, current_page, dialog):
        """Kitap bilgilerini günceller"""
        if not title:
            messagebox.showerror("Hata", "Kitap adı boş olamaz!")
            return
            
        try:
            total_pages = int(total_pages) if total_pages else None
            current_page = int(current_page) if current_page else 0
        except ValueError:
            messagebox.showerror("Hata", "Sayfa sayıları geçerli sayılar olmalıdır!")
            return
            
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''UPDATE books SET title=?, author=?, total_pages=?, current_page=?
                         WHERE id=?''', 
                         (title, author, total_pages, current_page, book_id))
            conn.commit()
            
        dialog.destroy()
        self.load_books()
        messagebox.showinfo("Başarılı", "Kitap bilgileri güncellendi!")

    def delete_book(self):
        """Seçili kitabı siler"""
        selected = self.books_tree.focus()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen silmek için bir kitap seçin!")
            return
            
        book_id = self.books_tree.item(selected)['values'][0]
        book_title = self.books_tree.item(selected)['values'][1]
        
        if not messagebox.askyesno("Onay", f"'{book_title}' adlı kitabı silmek istediğinize emin misiniz?"):
            return
            
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM books WHERE id=?", (book_id,))
            conn.commit()
            
        self.load_books()
        self.update_stats()
        messagebox.showinfo("Başarılı", "Kitap başarıyla silindi!")

    def record_progress_dialog(self):
        """Kitap okuma ilerlemesi kaydetme dialogu"""
        selected = self.books_tree.focus()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen ilerleme kaydetmek için bir kitap seçin!")
            return
            
        book_id = self.books_tree.item(selected)['values'][0]
        book_title = self.books_tree.item(selected)['values'][1]
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"İlerleme Kaydet - {book_title}")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Widget'lar
        ttk.Label(dialog, text="Okunan Sayfa Sayısı:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        pages_entry = ttk.Entry(dialog, width=40)
        pages_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Harcanan Süre (dakika):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        minutes_entry = ttk.Entry(dialog, width=40)
        minutes_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Butonlar
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            btn_frame, text="İptal", 
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, text="Kaydet", style="Accent.TButton",
            command=lambda: self.save_progress(
                book_id,
                pages_entry.get(),
                minutes_entry.get(),
                dialog
            )
        ).pack(side=tk.LEFT, padx=5)
        
        # Odaklanma
        pages_entry.focus_set()

    def save_progress(self, book_id, pages_read, minutes_spent, dialog):
        """Okuma ilerlemesini kaydeder"""
        try:
            pages_read = int(pages_read) if pages_read else 0
            minutes_spent = int(minutes_spent) if minutes_spent else None
            
            if pages_read <= 0:
                raise ValueError("Okunan sayfa sayısı pozitif olmalıdır")
                
            if minutes_spent is not None and minutes_spent <= 0:
                raise ValueError("Harcanan süre pozitif olmalıdır")
                
        except ValueError as e:
            messagebox.showerror("Hata", str(e))
            return
            
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Okuma oturumunu kaydet
            c.execute('''INSERT INTO reading_sessions (book_id, date, pages_read, minutes_spent)
                         VALUES (?, ?, ?, ?)''', (book_id, current_date, pages_read, minutes_spent))
            
            # Kitabın mevcut sayfasını güncelle
            c.execute('''UPDATE books SET current_page = current_page + ?, 
                         is_currently_reading=1
                         WHERE id=?''', (pages_read, book_id))
            
            conn.commit()
            
        dialog.destroy()
        self.load_books()
        self.update_stats()
        messagebox.showinfo("Başarılı", "Okuma ilerlemesi kaydedildi!")

    def show_book_details(self):
        """Kitap detaylarını gösterir"""
        selected = self.books_tree.focus()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen detaylarını görmek için bir kitap seçin!")
            return
            
        book_id = self.books_tree.item(selected)['values'][0]
        book = self.get_book_details(book_id)
        
        if not book:
            messagebox.showerror("Hata", "Kitap bilgileri alınamadı!")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Kitap Detayları - {book[1]}")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.geometry("600x400")
        
        # Notebook (tabbed interface)
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Genel bilgiler sekmesi
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="Genel Bilgiler")
        
        # Kitap bilgileri
        ttk.Label(general_frame, text="Kitap Adı:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(general_frame, text=book[1]).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(general_frame, text="Yazar:", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(general_frame, text=book[2] if book[2] else "-").grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(general_frame, text="Toplam Sayfa:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(general_frame, text=book[3] if book[3] else "-").grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(general_frame, text="Mevcut Sayfa:", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(general_frame, text=book[4]).grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(general_frame, text="İlerleme:", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        progress = (book[4] / book[3]) * 100 if book[3] else 0
        ttk.Label(general_frame, text=f"{progress:.1f}%").grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(general_frame, text="Durum:", font=("Segoe UI", 10, "bold")).grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        status = "Okuyor" if book[7] == 1 else "Bitirdi" if book[6] else "Okunacak"
        ttk.Label(general_frame, text=status).grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(general_frame, text="Başlama Tarihi:", font=("Segoe UI", 10, "bold")).grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(general_frame, text=book[5] if book[5] else "-").grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(general_frame, text="Bitiş Tarihi:", font=("Segoe UI", 10, "bold")).grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(general_frame, text=book[6] if book[6] else "-").grid(row=7, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(general_frame, text="Puan:", font=("Segoe UI", 10, "bold")).grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(general_frame, text=book[8] if book[8] is not None else "-").grid(row=8, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Notlar sekmesi
        notes_frame = ttk.Frame(notebook)
        notebook.add(notes_frame, text="Notlar")
        
        notes_text = tk.Text(notes_frame, wrap=tk.WORD, width=60, height=10)
        notes_text.insert(tk.END, book[9] if book[9] else "")
        notes_text.config(state=tk.DISABLED)
        notes_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Okuma geçmişi sekmesi
        history_frame = ttk.Frame(notebook)
        notebook.add(history_frame, text="Okuma Geçmişi")
        
        tree = ttk.Treeview(
            history_frame, 
            columns=("date", "pages", "minutes"), 
            show="headings"
        )
        
        tree.heading("date", text="Tarih")
        tree.heading("pages", text="Sayfa Sayısı")
        tree.heading("minutes", text="Dakika")
        
        tree.column("date", width=150)
        tree.column("pages", width=100, anchor=tk.CENTER)
        tree.column("minutes", width=100, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Geçmiş verilerini yükle
        history = self.get_book_reading_history(book_id)
        for session in history:
            tree.insert("", tk.END, values=(
                session[0], 
                session[1], 
                session[2] if session[2] else "-"
            ))

    def get_book_details(self, book_id):
        """Kitap detaylarını veritabanından alır"""
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''SELECT id, title, author, total_pages, current_page, 
                        start_date, end_date, is_currently_reading, rating, notes
                        FROM books WHERE id=?''', (book_id,))
            return c.fetchone()

    def get_book_reading_history(self, book_id):
        """Kitap okuma geçmişini getirir"""
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''SELECT date, pages_read, minutes_spent
                         FROM reading_sessions
                         WHERE book_id=?
                         ORDER BY date DESC''', (book_id,))
            return c.fetchall()

    # Makale işlemleri
    def load_articles(self):
        """Makaleleri veritabanından yükler ve treeview'da gösterir"""
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''SELECT id, title, author, source,
                        CASE 
                            WHEN is_read=1 THEN 'Okundu'
                            ELSE 'Okunacak'
                        END as status
                        FROM articles
                        ORDER BY 
                            CASE status
                                WHEN 'Okunacak' THEN 1
                                ELSE 2
                            END, added_date DESC''')
            
            articles = c.fetchall()
        
        # Treeview'ı temizle
        self.articles_tree.delete(*self.articles_tree.get_children())
        
        # Yeni verileri ekle
        for article in articles:
            self.articles_tree.insert("", tk.END, values=(
                article[0], article[1], article[2], article[3], article[4]
            ))

    def add_article_dialog(self):
        """Yeni makale ekleme dialog penceresi"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Yeni Makale Ekle")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Widget'lar
        ttk.Label(dialog, text="Makale Adı:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Yazar:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        author_entry = ttk.Entry(dialog, width=40)
        author_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Kaynak:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        source_entry = ttk.Entry(dialog, width=40)
        source_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="URL:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        url_entry = ttk.Entry(dialog, width=40)
        url_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Butonlar
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            btn_frame, text="İptal", 
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, text="Kaydet", style="Accent.TButton",
            command=lambda: self.save_new_article(
                title_entry.get(),
                author_entry.get(),
                source_entry.get(),
                url_entry.get(),
                dialog
            )
        ).pack(side=tk.LEFT, padx=5)
        
        # Odaklanma
        title_entry.focus_set()

    def save_new_article(self, title, author, source, url, dialog):
        """Yeni makaleyi veritabanına kaydeder"""
        if not title:
            messagebox.showerror("Hata", "Makale adı boş olamaz!")
            return
            
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO articles (title, author, source, url)
                         VALUES (?, ?, ?, ?)''', (title, author, source, url))
            conn.commit()
            
        dialog.destroy()
        self.load_articles()
        self.update_stats()
        messagebox.showinfo("Başarılı", "Makale başarıyla eklendi!")

    def edit_article_dialog(self):
        """Makale düzenleme dialog penceresi"""
        selected = self.articles_tree.focus()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen düzenlemek için bir makale seçin!")
            return
            
        article_id = self.articles_tree.item(selected)['values'][0]
        article = self.get_article_details(article_id)
        
        if not article:
            messagebox.showerror("Hata", "Makale bilgileri alınamadı!")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("Makale Düzenle")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Widget'lar
        ttk.Label(dialog, text="Makale Adı:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.insert(0, article[1])
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Yazar:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        author_entry = ttk.Entry(dialog, width=40)
        author_entry.insert(0, article[2] if article[2] else "")
        author_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Kaynak:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        source_entry = ttk.Entry(dialog, width=40)
        source_entry.insert(0, article[3] if article[3] else "")
        source_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="URL:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        url_entry = ttk.Entry(dialog, width=40)
        url_entry.insert(0, article[4] if article[4] else "")
        url_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Butonlar
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            btn_frame, text="İptal", 
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, text="Kaydet", style="Accent.TButton",
            command=lambda: self.update_article(
                article_id,
                title_entry.get(),
                author_entry.get(),
                source_entry.get(),
                url_entry.get(),
                dialog
            )
        ).pack(side=tk.LEFT, padx=5)
        
        # Odaklanma
        title_entry.focus_set()

    def update_article(self, article_id, title, author, source, url, dialog):
        """Makale bilgilerini günceller"""
        if not title:
            messagebox.showerror("Hata", "Makale adı boş olamaz!")
            return
            
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''UPDATE articles SET title=?, author=?, source=?, url=?
                         WHERE id=?''', 
                         (title, author, source, url, article_id))
            conn.commit()
            
        dialog.destroy()
        self.load_articles()
        messagebox.showinfo("Başarılı", "Makale bilgileri güncellendi!")

    def delete_article(self):
        """Seçili makaleyi siler"""
        selected = self.articles_tree.focus()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen silmek için bir makale seçin!")
            return
            
        article_id = self.articles_tree.item(selected)['values'][0]
        article_title = self.articles_tree.item(selected)['values'][1]
        
        if not messagebox.askyesno("Onay", f"'{article_title}' adlı makaleyi silmek istediğinize emin misiniz?"):
            return
            
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM articles WHERE id=?", (article_id,))
            conn.commit()
            
        self.load_articles()
        self.update_stats()
        messagebox.showinfo("Başarılı", "Makale başarıyla silindi!")

    def mark_article_as_read(self):
        """Makaleyi okundu olarak işaretler"""
        selected = self.articles_tree.focus()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen okundu olarak işaretlemek için bir makale seçin!")
            return
            
        article_id = self.articles_tree.item(selected)['values'][0]
        article_title = self.articles_tree.item(selected)['values'][1]
        
        # Puan ve notlar için dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Okundu İşaretle - {article_title}")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Puan (0-5):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        rating_entry = ttk.Entry(dialog, width=5)
        rating_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(dialog, text="Notlar:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        notes_entry = tk.Text(dialog, width=40, height=5, wrap=tk.WORD)
        notes_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Harcanan Süre (dakika):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        minutes_entry = ttk.Entry(dialog, width=5)
        minutes_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            btn_frame, text="İptal", 
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, text="Kaydet", style="Accent.TButton",
            command=lambda: self.save_article_read_status(
                article_id,
                rating_entry.get(),
                notes_entry.get("1.0", tk.END).strip(),
                minutes_entry.get(),
                dialog
            )
        ).pack(side=tk.LEFT, padx=5)
        
        rating_entry.focus_set()

    def save_article_read_status(self, article_id, rating, notes, minutes, dialog):
        """Makalenin okundu bilgisini kaydeder"""
        try:
            rating = int(rating) if rating else None
            if rating is not None and (rating < 0 or rating > 5):
                raise ValueError("Puan 0-5 arasında olmalıdır")
                
            minutes = int(minutes) if minutes else 0
            if minutes < 0:
                raise ValueError("Süre pozitif olmalıdır")
                
        except ValueError as e:
            messagebox.showerror("Hata", str(e))
            return
            
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Makaleyi okundu olarak işaretle
            c.execute('''UPDATE articles 
                         SET is_read=1, read_date=?, rating=?, notes=?
                         WHERE id=?''', 
                         (current_date, rating, notes, article_id))
            
            # Okuma oturumunu kaydet
            if minutes > 0:
                c.execute('''INSERT INTO article_reading_sessions (article_id, date, minutes_spent)
                             VALUES (?, ?, ?)''', 
                             (article_id, current_date, minutes))
            
            conn.commit()
            
        dialog.destroy()
        self.load_articles()
        self.update_stats()
        messagebox.showinfo("Başarılı", "Makale okundu olarak işaretlendi!")

    def show_article_details(self):
        """Makale detaylarını gösterir"""
        selected = self.articles_tree.focus()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen detaylarını görmek için bir makale seçin!")
            return
            
        article_id = self.articles_tree.item(selected)['values'][0]
        article = self.get_article_details(article_id)
        
        if not article:
            messagebox.showerror("Hata", "Makale bilgileri alınamadı!")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Makale Detayları - {article[1]}")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.geometry("600x400")
        
        # Notebook (tabbed interface)
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Genel bilgiler sekmesi
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="Genel Bilgiler")
        
        # Makale bilgileri
        ttk.Label(general_frame, text="Makale Adı:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(general_frame, text=article[1]).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(general_frame, text="Yazar:", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(general_frame, text=article[2] if article[2] else "-").grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(general_frame, text="Kaynak:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(general_frame, text=article[3] if article[3] else "-").grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(general_frame, text="URL:", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        url = article[4] if article[4] else "-"
        ttk.Label(general_frame, text=url).grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(general_frame, text="Durum:", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        status = "Okundu" if article[6] == 1 else "Okunacak"
        ttk.Label(general_frame, text=status).grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(general_frame, text="Okuma Tarihi:", font=("Segoe UI", 10, "bold")).grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(general_frame, text=article[5] if article[5] else "-").grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(general_frame, text="Puan:", font=("Segoe UI", 10, "bold")).grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(general_frame, text=article[7] if article[7] is not None else "-").grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Notlar sekmesi
        notes_frame = ttk.Frame(notebook)
        notebook.add(notes_frame, text="Notlar")
        
        notes_text = tk.Text(notes_frame, wrap=tk.WORD, width=60, height=10)
        notes_text.insert(tk.END, article[8] if article[8] else "")
        notes_text.config(state=tk.DISABLED)
        notes_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Okuma geçmişi sekmesi (sadece okunmuşsa)
        if article[6] == 1:
            history_frame = ttk.Frame(notebook)
            notebook.add(history_frame, text="Okuma Geçmişi")
            
            tree = ttk.Treeview(
                history_frame, 
                columns=("date", "minutes"), 
                show="headings"
            )
            
            tree.heading("date", text="Tarih")
            tree.heading("minutes", text="Dakika")
            
            tree.column("date", width=150)
            tree.column("minutes", width=100, anchor=tk.CENTER)
            
            scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Geçmiş verilerini yükle
            history = self.get_article_reading_history(article_id)
            for session in history:
                tree.insert("", tk.END, values=(session[0], session[1]))

    def get_article_details(self, article_id):
        """Makale detaylarını veritabanından alır"""
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''SELECT id, title, author, source, url, read_date, 
                        is_read, rating, notes FROM articles WHERE id=?''', (article_id,))
            return c.fetchone()

    def get_article_reading_history(self, article_id):
        """Makale okuma geçmişini getirir"""
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''SELECT date, minutes_spent
                         FROM article_reading_sessions
                         WHERE article_id=?
                         ORDER BY date DESC''', (article_id,))
            return c.fetchall()

    # İstatistik işlemleri
    def update_stats(self):
        """Hızlı istatistikleri günceller"""
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            
            # Kitap istatistikleri
            c.execute("SELECT COUNT(*) FROM books WHERE is_currently_reading=1")
            current_books = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM books WHERE is_currently_reading=0 AND end_date IS NOT NULL")
            completed_books = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM books WHERE is_currently_reading=0 AND start_date IS NULL")
            unread_books = c.fetchone()[0]
            
            # Makale istatistikleri
            c.execute("SELECT COUNT(*) FROM articles WHERE is_read=1")
            read_articles = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM articles WHERE is_read=0")
            unread_articles = c.fetchone()[0]
            
        # Etiketleri güncelle
        self.current_books_label.config(text=f"Okuyor: {current_books}")
        self.completed_books_label.config(text=f"Bitirdi: {completed_books}")
        self.unread_books_label.config(text=f"Okunacak: {unread_books}")
        self.read_articles_label.config(text=f"Okunan Makaleler: {read_articles}")
        self.unread_articles_label.config(text=f"Okunacak Makaleler: {unread_articles}")

    def plot_reading_activity(self, days=30):
        """Okuma aktivitesini görselleştirir"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            
            # Kitap okuma aktivitesi
            c.execute('''SELECT date, SUM(pages_read) as pages
                         FROM reading_sessions
                         WHERE date BETWEEN ? AND ?
                         GROUP BY date
                         ORDER BY date''', 
                         (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
            
            book_data = c.fetchall()
            
            # Makale okuma aktivitesi
            c.execute('''SELECT date, SUM(minutes_spent) as minutes
                         FROM article_reading_sessions
                         WHERE date BETWEEN ? AND ?
                         GROUP BY date
                         ORDER BY date''', 
                         (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
            
            article_data = c.fetchall()
        
        # Grafik çerçevesini temizle
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Verileri işle
        book_dates = [datetime.strptime(row[0], '%Y-%m-%d') for row in book_data]
        book_pages = [row[1] for row in book_data]
        
        article_dates = [datetime.strptime(row[0], '%Y-%m-%d') for row in article_data]
        article_minutes = [row[1] for row in article_data]
        
        # Grafik oluştur
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        
        # Kitap okuma grafiği
        if book_dates:
            ax1.bar(book_dates, book_pages, color='skyblue', label='Okunan Sayfalar')
            ax1.set_title(f'Son {days} Günlük Kitap Okuma Aktivitesi')
            ax1.set_ylabel('Sayfa Sayısı')
            ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
            ax1.legend()
        else:
            ax1.text(0.5, 0.5, 'Veri yok', ha='center', va='center')
            ax1.set_title(f'Son {days} Günlük Kitap Okuma Aktivitesi')
        
        # Makale okuma grafiği
        if article_dates:
            ax2.bar(article_dates, article_minutes, color='lightgreen', label='Harcanan Dakikalar')
            ax2.set_title(f'Son {days} Günlük Makale Okuma Aktivitesi')
            ax2.set_ylabel('Dakika')
            ax2.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
            ax2.legend()
        else:
            ax2.text(0.5, 0.5, 'Veri yok', ha='center', va='center')
            ax2.set_title(f'Son {days} Günlük Makale Okuma Aktivitesi')
        
        plt.tight_layout()
        
        # Grafiği TKinter'a göm
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Yardımcı fonksiyonlar
    def show_books_tab(self):
        """Kitaplar sekmesini gösterir"""
        self.notebook.select(self.books_frame)

    def show_articles_tab(self):
        """Makaleler sekmesini gösterir"""
        self.notebook.select(self.articles_frame)

def main():
    root = tk.Tk()
    app = ReadingTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
