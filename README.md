# FlaskBlog

A modern blog application built with Flask, featuring a clean UI and powerful admin tools.

![FlaskBlog Light Theme](/images/Light.png)
[Watch demo on YouTube](https://youtu.be/WyIpAlSp2RM) — [See screenshots (mobile/desktop, dark/light)](https://github.com/DogukanUrker/flaskBlog/tree/main/images)

## ✨ Features

- **User System** - Registration, login, profiles with custom avatars
- **Rich Editor** - [Milkdown](https://milkdown.dev/) editor for creating beautiful posts
- **Admin Panel** - Full control over users, posts, and comments
- **Dark/Light Themes** - Automatic theme switching
- **Categories** - Organize posts by topics
- **Search** - Find posts quickly
- **Responsive Design** - Works great on all devices
- **Advanced Logging** - Powered by [Tamga](https://github.com/dogukanurker/tamga) logger

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [astral/uv](https://docs.astral.sh/uv/)

### Installation

```bash
# Clone the repository
git clone https://github.com/DogukanUrker/flaskBlog.git
cd flaskBlog

# Install dependencies and run
make install-app
make run
```

Visit `http://localhost:1283` in your browser.

### Default Admin Account

- Username: `admin`
- Password: `admin`

### Makefile Commands

```bash
make help          # Show all available commands
make install       # Install all dependencies (app + dev + test + Playwright)
make install-app   # Install app dependencies only
make run           # Run the Flask application
make test          # Run E2E tests (parallel)
make test-slow     # Run tests with browser visible (slow-mo)
make lint          # Format and lint code (auto-fix)
make ci            # Run CI checks
make clean         # Remove cache files
```

### Running Tests

```bash
make install       # Install all dependencies including test deps
make test          # Run E2E tests (parallel)
```

See [tests/README.md](tests/README.md) for details.

## 🛠️ Tech Stack

**Backend:** Flask, SQLite3, WTForms, Passlib \
**Frontend:** TailwindCSS, jQuery, Summer Note Editor \
**Icons:** Tabler Icons

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Doğukan Ürker** \
[Website](https://dogukanurker.com) | [Email](mailto:dogukanurker@icloud.com)

---

⭐ If you find this project useful, please consider giving it a star!
