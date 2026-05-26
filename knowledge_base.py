PREREQUISITES_KB = {

    # ── JAVASCRIPT ECOSYSTEM ──────────────────
    "node": {
        "name": "Node.js",
        "recommended_version": "v20 LTS",
        "windows_download_url": "https://nodejs.org/en/download",
        "mac_download_url": "https://nodejs.org/en/download",
        "linux_download_url": "https://nodejs.org/en/download",
        "windows_install_command": "winget install OpenJS.NodeJS.LTS",
        "mac_install_command": "brew install node",
        "linux_install_command": "sudo apt-get install -y nodejs npm",
        "verify_command": "node --version",
        "description": "JavaScript runtime engine"
    },
    "nodejs": {
        "name": "Node.js",
        "recommended_version": "v20 LTS",
        "windows_download_url": "https://nodejs.org/en/download",
        "mac_download_url": "https://nodejs.org/en/download",
        "linux_download_url": "https://nodejs.org/en/download",
        "windows_install_command": "winget install OpenJS.NodeJS.LTS",
        "mac_install_command": "brew install node",
        "linux_install_command": "sudo apt-get install -y nodejs npm",
        "verify_command": "node --version",
        "description": "JavaScript runtime engine"
    },
    "npm": {
        "name": "npm",
        "recommended_version": "comes with Node.js",
        "windows_download_url": "https://nodejs.org/en/download",
        "mac_download_url": "https://nodejs.org/en/download",
        "linux_download_url": "https://nodejs.org/en/download",
        "windows_install_command": "winget install OpenJS.NodeJS.LTS",
        "mac_install_command": "brew install node",
        "linux_install_command": "sudo apt-get install -y npm",
        "verify_command": "npm --version",
        "description": "Node.js package manager"
    },
    "yarn": {
        "name": "Yarn",
        "recommended_version": "1.22+ or 4.x",
        "windows_download_url": "https://yarnpkg.com/getting-started/install",
        "mac_download_url": "https://yarnpkg.com/getting-started/install",
        "linux_download_url": "https://yarnpkg.com/getting-started/install",
        "windows_install_command": "npm install -g yarn",
        "mac_install_command": "npm install -g yarn",
        "linux_install_command": "npm install -g yarn",
        "verify_command": "yarn --version",
        "description": "Fast reliable Node.js package manager"
    },
    "pnpm": {
        "name": "pnpm",
        "recommended_version": "8.x+",
        "windows_download_url": "https://pnpm.io/installation",
        "mac_download_url": "https://pnpm.io/installation",
        "linux_download_url": "https://pnpm.io/installation",
        "windows_install_command": "npm install -g pnpm",
        "mac_install_command": "npm install -g pnpm",
        "linux_install_command": "npm install -g pnpm",
        "verify_command": "pnpm --version",
        "description": "Efficient disk-space saving package manager"
    },
    "bun": {
        "name": "Bun",
        "recommended_version": "latest",
        "windows_download_url": "https://bun.sh/docs/installation",
        "mac_download_url": "https://bun.sh",
        "linux_download_url": "https://bun.sh",
        "windows_install_command": "powershell -c \"irm bun.sh/install.ps1|iex\"",
        "mac_install_command": "curl -fsSL https://bun.sh/install | bash",
        "linux_install_command": "curl -fsSL https://bun.sh/install | bash",
        "verify_command": "bun --version",
        "description": "Fast all-in-one JavaScript runtime and package manager"
    },
    "deno": {
        "name": "Deno",
        "recommended_version": "2.x",
        "windows_download_url": "https://deno.land/#installation",
        "mac_download_url": "https://deno.land/#installation",
        "linux_download_url": "https://deno.land/#installation",
        "windows_install_command": "winget install DenoLand.Deno",
        "mac_install_command": "brew install deno",
        "linux_install_command": "curl -fsSL https://deno.land/install.sh | sh",
        "verify_command": "deno --version",
        "description": "Secure JavaScript and TypeScript runtime"
    },

    # ── PYTHON ECOSYSTEM ──────────────────────
    "python": {
        "name": "Python",
        "recommended_version": "3.11+",
        "windows_download_url": "https://www.python.org/downloads",
        "mac_download_url": "https://www.python.org/downloads",
        "linux_download_url": "https://www.python.org/downloads",
        "windows_install_command": "winget install Python.Python.3.11",
        "mac_install_command": "brew install python",
        "linux_install_command": "sudo apt-get install -y python3 python3-pip",
        "verify_command": "python --version",
        "description": "General purpose programming language"
    },
    "python3": {
        "name": "Python 3",
        "recommended_version": "3.11+",
        "windows_download_url": "https://www.python.org/downloads",
        "mac_download_url": "https://www.python.org/downloads",
        "linux_download_url": "https://www.python.org/downloads",
        "windows_install_command": "winget install Python.Python.3.11",
        "mac_install_command": "brew install python",
        "linux_install_command": "sudo apt-get install -y python3 python3-pip",
        "verify_command": "python3 --version",
        "description": "General purpose programming language"
    },
    "pip": {
        "name": "pip",
        "recommended_version": "comes with Python",
        "windows_download_url": "https://www.python.org/downloads",
        "mac_download_url": "https://www.python.org/downloads",
        "linux_download_url": "https://www.python.org/downloads",
        "windows_install_command": "python -m ensurepip --upgrade",
        "mac_install_command": "python3 -m ensurepip --upgrade",
        "linux_install_command": "sudo apt-get install -y python3-pip",
        "verify_command": "pip --version",
        "description": "Python package manager"
    },
    "poetry": {
        "name": "Poetry",
        "recommended_version": "1.7+",
        "windows_download_url": "https://python-poetry.org/docs",
        "mac_download_url": "https://python-poetry.org/docs",
        "linux_download_url": "https://python-poetry.org/docs",
        "windows_install_command": "pip install poetry",
        "mac_install_command": "brew install poetry",
        "linux_install_command": "pip install poetry",
        "verify_command": "poetry --version",
        "description": "Python dependency management and packaging tool"
    },
    "conda": {
        "name": "Conda (Miniconda)",
        "recommended_version": "latest",
        "windows_download_url": "https://docs.conda.io/en/latest/miniconda.html",
        "mac_download_url": "https://docs.conda.io/en/latest/miniconda.html",
        "linux_download_url": "https://docs.conda.io/en/latest/miniconda.html",
        "windows_install_command": "winget install Anaconda.Miniconda3",
        "mac_install_command": "brew install --cask miniconda",
        "linux_install_command": "wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && bash Miniconda3-latest-Linux-x86_64.sh",
        "verify_command": "conda --version",
        "description": "Python environment and package manager for data science"
    },

    # ── SYSTEMS LANGUAGES ─────────────────────
    "rust": {
        "name": "Rust",
        "recommended_version": "latest stable",
        "windows_download_url": "https://rustup.rs",
        "mac_download_url": "https://rustup.rs",
        "linux_download_url": "https://rustup.rs",
        "windows_install_command": "winget install Rustlang.Rustup",
        "mac_install_command": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
        "linux_install_command": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
        "verify_command": "rustc --version",
        "description": "Systems programming language focused on safety and speed"
    },
    "cargo": {
        "name": "Cargo",
        "recommended_version": "comes with Rust",
        "windows_download_url": "https://rustup.rs",
        "mac_download_url": "https://rustup.rs",
        "linux_download_url": "https://rustup.rs",
        "windows_install_command": "winget install Rustlang.Rustup",
        "mac_install_command": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
        "linux_install_command": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
        "verify_command": "cargo --version",
        "description": "Rust package manager — included with Rust"
    },
    "go": {
        "name": "Go",
        "recommended_version": "1.21+",
        "windows_download_url": "https://go.dev/dl",
        "mac_download_url": "https://go.dev/dl",
        "linux_download_url": "https://go.dev/dl",
        "windows_install_command": "winget install GoLang.Go",
        "mac_install_command": "brew install go",
        "linux_install_command": "sudo apt-get install -y golang-go",
        "verify_command": "go version",
        "description": "Fast statically typed language by Google"
    },
    "gcc": {
        "name": "GCC Compiler",
        "recommended_version": "12+",
        "windows_download_url": "https://www.mingw-w64.org/downloads",
        "mac_download_url": "https://gcc.gnu.org",
        "linux_download_url": "https://gcc.gnu.org",
        "windows_install_command": "winget install GnuWin32.Gcc",
        "mac_install_command": "xcode-select --install",
        "linux_install_command": "sudo apt-get install -y build-essential",
        "verify_command": "gcc --version",
        "description": "GNU C/C++ compiler"
    },
    "cmake": {
        "name": "CMake",
        "recommended_version": "3.25+",
        "windows_download_url": "https://cmake.org/download",
        "mac_download_url": "https://cmake.org/download",
        "linux_download_url": "https://cmake.org/download",
        "windows_install_command": "winget install Kitware.CMake",
        "mac_install_command": "brew install cmake",
        "linux_install_command": "sudo apt-get install -y cmake",
        "verify_command": "cmake --version",
        "description": "Cross-platform build system generator"
    },
    "make": {
        "name": "Make",
        "recommended_version": "4.x",
        "windows_download_url": "https://gnuwin32.sourceforge.net/packages/make.htm",
        "mac_download_url": "https://www.gnu.org/software/make",
        "linux_download_url": "https://www.gnu.org/software/make",
        "windows_install_command": "winget install GnuWin32.Make",
        "mac_install_command": "xcode-select --install",
        "linux_install_command": "sudo apt-get install -y make",
        "verify_command": "make --version",
        "description": "Build automation tool"
    },

    # ── JVM LANGUAGES ─────────────────────────
    "java": {
        "name": "Java JDK",
        "recommended_version": "17 LTS",
        "windows_download_url": "https://adoptium.net/temurin/releases",
        "mac_download_url": "https://adoptium.net/temurin/releases",
        "linux_download_url": "https://adoptium.net/temurin/releases",
        "windows_install_command": "winget install EclipseAdoptium.Temurin.17.JDK",
        "mac_install_command": "brew install --cask temurin@17",
        "linux_install_command": "sudo apt-get install -y openjdk-17-jdk",
        "verify_command": "java --version",
        "description": "Java Development Kit"
    },
    "maven": {
        "name": "Apache Maven",
        "recommended_version": "3.9+",
        "windows_download_url": "https://maven.apache.org/download.cgi",
        "mac_download_url": "https://maven.apache.org/download.cgi",
        "linux_download_url": "https://maven.apache.org/download.cgi",
        "windows_install_command": "winget install Apache.Maven",
        "mac_install_command": "brew install maven",
        "linux_install_command": "sudo apt-get install -y maven",
        "verify_command": "mvn --version",
        "description": "Java build and dependency management tool"
    },
    "gradle": {
        "name": "Gradle",
        "recommended_version": "8.x",
        "windows_download_url": "https://gradle.org/install",
        "mac_download_url": "https://gradle.org/install",
        "linux_download_url": "https://gradle.org/install",
        "windows_install_command": "winget install Gradle.Gradle",
        "mac_install_command": "brew install gradle",
        "linux_install_command": "sudo apt-get install -y gradle",
        "verify_command": "gradle --version",
        "description": "Build automation tool for Java/Android projects"
    },
    "kotlin": {
        "name": "Kotlin",
        "recommended_version": "1.9+",
        "windows_download_url": "https://kotlinlang.org/docs/getting-started.html",
        "mac_download_url": "https://kotlinlang.org/docs/getting-started.html",
        "linux_download_url": "https://kotlinlang.org/docs/getting-started.html",
        "windows_install_command": "winget install JetBrains.Kotlin.Compiler",
        "mac_install_command": "brew install kotlin",
        "linux_install_command": "sudo apt-get install -y kotlin",
        "verify_command": "kotlinc -version",
        "description": "Modern statically typed JVM language by JetBrains"
    },
    "scala": {
        "name": "Scala",
        "recommended_version": "3.x",
        "windows_download_url": "https://www.scala-lang.org/download",
        "mac_download_url": "https://www.scala-lang.org/download",
        "linux_download_url": "https://www.scala-lang.org/download",
        "windows_install_command": "winget install EPFL.Scala",
        "mac_install_command": "brew install scala",
        "linux_install_command": "sudo apt-get install -y scala",
        "verify_command": "scala --version",
        "description": "Functional and object-oriented JVM language"
    },

    # ── MOBILE / CROSS-PLATFORM ───────────────
    "flutter": {
        "name": "Flutter",
        "recommended_version": "3.x",
        "windows_download_url": "https://flutter.dev/docs/get-started/install/windows",
        "mac_download_url": "https://flutter.dev/docs/get-started/install/macos",
        "linux_download_url": "https://flutter.dev/docs/get-started/install/linux",
        "windows_install_command": "winget install Google.Flutter",
        "mac_install_command": "brew install --cask flutter",
        "linux_install_command": "sudo snap install flutter --classic",
        "verify_command": "flutter --version",
        "description": "Google's UI framework for cross-platform apps"
    },
    "dart": {
        "name": "Dart",
        "recommended_version": "3.x",
        "windows_download_url": "https://dart.dev/get-dart",
        "mac_download_url": "https://dart.dev/get-dart",
        "linux_download_url": "https://dart.dev/get-dart",
        "windows_install_command": "winget install Google.Dart",
        "mac_install_command": "brew install dart",
        "linux_install_command": "sudo apt-get install -y dart",
        "verify_command": "dart --version",
        "description": "Language optimized for client-side development"
    },
    "swift": {
        "name": "Swift",
        "recommended_version": "5.9+",
        "windows_download_url": "https://www.swift.org/download",
        "mac_download_url": "https://developer.apple.com/xcode",
        "linux_download_url": "https://www.swift.org/download",
        "windows_install_command": "winget install Swift.Toolchain",
        "mac_install_command": "xcode-select --install",
        "linux_install_command": "sudo apt-get install -y swift",
        "verify_command": "swift --version",
        "description": "Apple's programming language for iOS and macOS"
    },

    # ── FUNCTIONAL LANGUAGES ──────────────────
    "elixir": {
        "name": "Elixir",
        "recommended_version": "1.16+",
        "windows_download_url": "https://elixir-lang.org/install.html",
        "mac_download_url": "https://elixir-lang.org/install.html",
        "linux_download_url": "https://elixir-lang.org/install.html",
        "windows_install_command": "winget install ElixirLang.Elixir",
        "mac_install_command": "brew install elixir",
        "linux_install_command": "sudo apt-get install -y elixir",
        "verify_command": "elixir --version",
        "description": "Dynamic functional language for scalable applications"
    },
    "erlang": {
        "name": "Erlang/OTP",
        "recommended_version": "26+",
        "windows_download_url": "https://www.erlang.org/downloads",
        "mac_download_url": "https://www.erlang.org/downloads",
        "linux_download_url": "https://www.erlang.org/downloads",
        "windows_install_command": "winget install Erlang.OTP",
        "mac_install_command": "brew install erlang",
        "linux_install_command": "sudo apt-get install -y erlang",
        "verify_command": "erl -s halt",
        "description": "Concurrent fault-tolerant programming platform"
    },
    "haskell": {
        "name": "Haskell (GHCup)",
        "recommended_version": "GHC 9.6+",
        "windows_download_url": "https://www.haskell.org/ghcup",
        "mac_download_url": "https://www.haskell.org/ghcup",
        "linux_download_url": "https://www.haskell.org/ghcup",
        "windows_install_command": "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; Invoke-Command -ScriptBlock ([ScriptBlock]::Create((Invoke-WebRequest https://www.haskell.org/ghcup/sh/bootstrap-haskell.ps1 -UseBasicParsing))) -ArgumentList $true",
        "mac_install_command": "curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh",
        "linux_install_command": "curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh",
        "verify_command": "ghc --version",
        "description": "Purely functional programming language"
    },

    # ── OTHER LANGUAGES ───────────────────────
    "ruby": {
        "name": "Ruby",
        "recommended_version": "3.2+",
        "windows_download_url": "https://rubyinstaller.org/downloads",
        "mac_download_url": "https://www.ruby-lang.org/en/downloads",
        "linux_download_url": "https://www.ruby-lang.org/en/downloads",
        "windows_install_command": "winget install RubyInstallerTeam.RubyWithDevKit.3.2",
        "mac_install_command": "brew install ruby",
        "linux_install_command": "sudo apt-get install -y ruby-full",
        "verify_command": "ruby --version",
        "description": "Dynamic open source programming language"
    },
    "php": {
        "name": "PHP",
        "recommended_version": "8.2+",
        "windows_download_url": "https://windows.php.net/download",
        "mac_download_url": "https://www.php.net/downloads",
        "linux_download_url": "https://www.php.net/downloads",
        "windows_install_command": "winget install PHP.PHP.8.2",
        "mac_install_command": "brew install php",
        "linux_install_command": "sudo apt-get install -y php8.2 php8.2-cli",
        "verify_command": "php --version",
        "description": "Server-side scripting language"
    },
    "composer": {
        "name": "Composer",
        "recommended_version": "2.x",
        "windows_download_url": "https://getcomposer.org/download",
        "mac_download_url": "https://getcomposer.org/download",
        "linux_download_url": "https://getcomposer.org/download",
        "windows_install_command": "winget install Composer.Composer",
        "mac_install_command": "brew install composer",
        "linux_install_command": "sudo apt-get install -y composer",
        "verify_command": "composer --version",
        "description": "PHP dependency manager"
    },
    "perl": {
        "name": "Perl",
        "recommended_version": "5.36+",
        "windows_download_url": "https://strawberryperl.com",
        "mac_download_url": "https://www.perl.org/get.html",
        "linux_download_url": "https://www.perl.org/get.html",
        "windows_install_command": "winget install StrawberryPerl.StrawberryPerl",
        "mac_install_command": "brew install perl",
        "linux_install_command": "sudo apt-get install -y perl",
        "verify_command": "perl --version",
        "description": "High-level general purpose programming language"
    },
    "lua": {
        "name": "Lua",
        "recommended_version": "5.4",
        "windows_download_url": "https://luabinaries.sourceforge.net",
        "mac_download_url": "https://www.lua.org/download.html",
        "linux_download_url": "https://www.lua.org/download.html",
        "windows_install_command": "winget install DEVCOM.Lua",
        "mac_install_command": "brew install lua",
        "linux_install_command": "sudo apt-get install -y lua5.4",
        "verify_command": "lua -v",
        "description": "Lightweight embeddable scripting language"
    },
    "julia": {
        "name": "Julia",
        "recommended_version": "1.10+",
        "windows_download_url": "https://julialang.org/downloads",
        "mac_download_url": "https://julialang.org/downloads",
        "linux_download_url": "https://julialang.org/downloads",
        "windows_install_command": "winget install Julialang.Julia",
        "mac_install_command": "brew install julia",
        "linux_install_command": "curl -fsSL https://install.julialang.org | sh",
        "verify_command": "julia --version",
        "description": "High-performance language for scientific computing"
    },

    # ── DATABASES ─────────────────────────────
    "postgresql": {
        "name": "PostgreSQL",
        "recommended_version": "15+",
        "windows_download_url": "https://www.postgresql.org/download/windows",
        "mac_download_url": "https://www.postgresql.org/download/macosx",
        "linux_download_url": "https://www.postgresql.org/download/linux",
        "windows_install_command": "winget install PostgreSQL.PostgreSQL.15",
        "mac_install_command": "brew install postgresql@15",
        "linux_install_command": "sudo apt-get install -y postgresql postgresql-contrib",
        "verify_command": "psql --version",
        "description": "Powerful open source relational database"
    },
    "mysql": {
        "name": "MySQL",
        "recommended_version": "8.0+",
        "windows_download_url": "https://dev.mysql.com/downloads/installer",
        "mac_download_url": "https://dev.mysql.com/downloads/mysql",
        "linux_download_url": "https://dev.mysql.com/downloads/mysql",
        "windows_install_command": "winget install Oracle.MySQL",
        "mac_install_command": "brew install mysql",
        "linux_install_command": "sudo apt-get install -y mysql-server",
        "verify_command": "mysql --version",
        "description": "Popular open source relational database"
    },
    "mongodb": {
        "name": "MongoDB",
        "recommended_version": "7.0+",
        "windows_download_url": "https://www.mongodb.com/try/download/community",
        "mac_download_url": "https://www.mongodb.com/try/download/community",
        "linux_download_url": "https://www.mongodb.com/try/download/community",
        "windows_install_command": "winget install MongoDB.Server",
        "mac_install_command": "brew install mongodb-community",
        "linux_install_command": "sudo apt-get install -y mongodb",
        "verify_command": "mongod --version",
        "description": "NoSQL document database"
    },
    "redis": {
        "name": "Redis",
        "recommended_version": "7.0+",
        "windows_download_url": "https://redis.io/downloads",
        "mac_download_url": "https://redis.io/downloads",
        "linux_download_url": "https://redis.io/downloads",
        "windows_install_command": "winget install Redis.Redis",
        "mac_install_command": "brew install redis",
        "linux_install_command": "sudo apt-get install -y redis-server",
        "verify_command": "redis-cli --version",
        "description": "In-memory data store for caching and sessions"
    },
    "sqlite": {
        "name": "SQLite",
        "recommended_version": "3.40+",
        "windows_download_url": "https://sqlite.org/download.html",
        "mac_download_url": "https://sqlite.org/download.html",
        "linux_download_url": "https://sqlite.org/download.html",
        "windows_install_command": "winget install SQLite.SQLite",
        "mac_install_command": "brew install sqlite",
        "linux_install_command": "sudo apt-get install -y sqlite3",
        "verify_command": "sqlite3 --version",
        "description": "Lightweight embedded SQL database engine"
    },

    # ── DEVOPS & INFRASTRUCTURE ───────────────
    "git": {
        "name": "Git",
        "recommended_version": "2.40+",
        "windows_download_url": "https://git-scm.com/download/win",
        "mac_download_url": "https://git-scm.com/download/mac",
        "linux_download_url": "https://git-scm.com/download/linux",
        "windows_install_command": "winget install Git.Git",
        "mac_install_command": "brew install git",
        "linux_install_command": "sudo apt-get install -y git",
        "verify_command": "git --version",
        "description": "Distributed version control system"
    },
    "docker": {
        "name": "Docker",
        "recommended_version": "latest",
        "windows_download_url": "https://docs.docker.com/desktop/install/windows-install",
        "mac_download_url": "https://docs.docker.com/desktop/install/mac-install",
        "linux_download_url": "https://docs.docker.com/engine/install",
        "windows_install_command": "winget install Docker.DockerDesktop",
        "mac_install_command": "brew install --cask docker",
        "linux_install_command": "sudo apt-get install -y docker.io docker-compose",
        "verify_command": "docker --version",
        "description": "Container platform for building and running applications"
    },
    "terraform": {
        "name": "Terraform",
        "recommended_version": "1.6+",
        "windows_download_url": "https://developer.hashicorp.com/terraform/install",
        "mac_download_url": "https://developer.hashicorp.com/terraform/install",
        "linux_download_url": "https://developer.hashicorp.com/terraform/install",
        "windows_install_command": "winget install Hashicorp.Terraform",
        "mac_install_command": "brew install terraform",
        "linux_install_command": "sudo apt-get install -y terraform",
        "verify_command": "terraform --version",
        "description": "Infrastructure as code tool by HashiCorp"
    },
    "ansible": {
        "name": "Ansible",
        "recommended_version": "2.15+",
        "windows_download_url": "https://docs.ansible.com/ansible/latest/installation_guide",
        "mac_download_url": "https://docs.ansible.com/ansible/latest/installation_guide",
        "linux_download_url": "https://docs.ansible.com/ansible/latest/installation_guide",
        "windows_install_command": "pip install ansible",
        "mac_install_command": "brew install ansible",
        "linux_install_command": "sudo apt-get install -y ansible",
        "verify_command": "ansible --version",
        "description": "IT automation and configuration management tool"
    },
    "kubectl": {
        "name": "kubectl",
        "recommended_version": "latest",
        "windows_download_url": "https://kubernetes.io/docs/tasks/tools/install-kubectl-windows",
        "mac_download_url": "https://kubernetes.io/docs/tasks/tools/install-kubectl-macos",
        "linux_download_url": "https://kubernetes.io/docs/tasks/tools/install-kubectl-linux",
        "windows_install_command": "winget install Kubernetes.kubectl",
        "mac_install_command": "brew install kubectl",
        "linux_install_command": "sudo apt-get install -y kubectl",
        "verify_command": "kubectl version --client",
        "description": "Kubernetes command-line tool"
    },
    "helm": {
        "name": "Helm",
        "recommended_version": "3.x",
        "windows_download_url": "https://helm.sh/docs/intro/install",
        "mac_download_url": "https://helm.sh/docs/intro/install",
        "linux_download_url": "https://helm.sh/docs/intro/install",
        "windows_install_command": "winget install Helm.Helm",
        "mac_install_command": "brew install helm",
        "linux_install_command": "curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash",
        "verify_command": "helm version",
        "description": "Kubernetes package manager"
    },
    "nginx": {
        "name": "Nginx",
        "recommended_version": "1.24+",
        "windows_download_url": "https://nginx.org/en/download.html",
        "mac_download_url": "https://nginx.org/en/download.html",
        "linux_download_url": "https://nginx.org/en/download.html",
        "windows_install_command": "winget install Nginx.Nginx",
        "mac_install_command": "brew install nginx",
        "linux_install_command": "sudo apt-get install -y nginx",
        "verify_command": "nginx -v",
        "description": "High-performance web server and reverse proxy"
    },

    # ── BUILD & PACKAGE MANAGEMENT ────────────
    "nvm": {
        "name": "nvm (Node Version Manager)",
        "recommended_version": "latest",
        "windows_download_url": "https://github.com/coreybutler/nvm-windows/releases",
        "mac_download_url": "https://github.com/nvm-sh/nvm",
        "linux_download_url": "https://github.com/nvm-sh/nvm",
        "windows_install_command": "winget install CoreyButler.NVMforWindows",
        "mac_install_command": "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash",
        "linux_install_command": "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash",
        "verify_command": "nvm --version",
        "description": "Manage multiple Node.js versions"
    },
}

def get_prerequisite(name: str) -> dict | None:
    key = name.lower().strip()
    direct = PREREQUISITES_KB.get(key)
    if direct:
        return direct
    for kb_key, kb_value in PREREQUISITES_KB.items():
        if kb_key in key or key in kb_key:
            return kb_value
    return None

def get_os_specific_data(prereq: dict, os: str) -> dict:
    os_lower = os.lower()
    if "windows" in os_lower:
        return {
            "download_url": prereq["windows_download_url"],
            "install_command": prereq["windows_install_command"],
        }
    elif "mac" in os_lower or "macos" in os_lower or "darwin" in os_lower:
        return {
            "download_url": prereq["mac_download_url"],
            "install_command": prereq["mac_install_command"],
        }
    else:
        return {
            "download_url": prereq["linux_download_url"],
            "install_command": prereq["linux_install_command"],
        }
