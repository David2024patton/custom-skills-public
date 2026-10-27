# Knowledge digest: python
Source: https://github.com/vinta/awesome-python
Generated: 2026-10-23T23:56:17Z
Load ONLY when working in this language/domain.

---

Directory structure:
└── vinta-awesome-python/
    ├── README.md
    ├── AGENTS.md
    ├── CLAUDE.md
    ├── CODE_OF_CONDUCT.md
    ├── CONTRIBUTING.md
    ├── DESIGN.md
    ├── LICENSE
    ├── Makefile
    ├── pyproject.toml
    ├── SPONSORSHIP.md
    ├── uv.lock
    ├── docs/
    │   ├── audit-logs.md
    │   └── adr/
    │       └── 0001-shortlist-not-catalog.md
    ├── website/
    │   ├── build.py
    │   ├── fetch_github_stars.py
    │   ├── fetch_pypi_downloads_via_bigquery.py
    │   ├── fetch_pypi_downloads_via_clickpy.py
    │   ├── fetch_pypi_downloads_via_pepy.py
    │   ├── readme_parser.py
    │   ├── data/
    │   │   └── pypi_name_overrides.json
    │   ├── static/
    │   │   ├── main.js
    │   │   └── style.css
    │   ├── templates/
    │   │   ├── _sponsor_band.html
    │   │   ├── base.html
    │   │   ├── category.html
    │   │   ├── index.html
    │   │   ├── llms.txt
    │   │   ├── redirect.html
    │   │   └── sponsorship.html
    │   └── tests/
    │       ├── test_build.py
    │       ├── test_fetch_github_stars.py
    │       ├── test_preview_verdicts.py
    │       ├── test_readme_parser.py
    │       └── test_scan_github_stars.py
    ├── .claude/
    │   └── skills/
    │       ├── audit-the-list/
    │       │   ├── SKILL.md
    │       │   └── scripts/
    │       │       └── audit_priority.py
    │       ├── preview-verdicts/
    │       │   ├── SKILL.md
    │       │   └── template.html
    │       ├── review-prs/
    │       │   └── SKILL.md
    │       └── scan-github-stars/
    │           ├── SKILL.md
    │           └── scripts/
    │               └── scan_github_stars.py
    └── .github/
        ├── FUNDING.yml
        ├── PULL_REQUEST_TEMPLATE.md
        └── workflows/
            ├── ci.yml
            └── deploy-website.yml

================================================
FILE: README.md
================================================
# [Awesome Python](https://awesome-python.com/)

An opinionated guide to the best Python frameworks, libraries, and tools.

**Visit the [website](https://awesome-python.com/) to search and filter projects more easily.**

## **Sponsors**

- [iPulse AI](https://ipulseai.com?utm_source=awesome-python&utm_medium=sponsorship&utm_campaign=sponsor&utm_content=readme) - Open Agentic Investment Research Platform. Inspect deep multi-agent market forecasts and stock picks.

> Sponsor slots open, from $99/month. The **#10 most-starred repo on GitHub**. Put your product in front of Python developers. [Become a sponsor](https://awesome-python.com/sponsorship/).

## Categories

**AI & ML**

- [AI and Agents](#ai-and-agents)
- [Deep Learning](#deep-learning)
- [Machine Learning](#machine-learning)
- [Natural Language Processing](#natural-language-processing)
- [Computer Vision](#computer-vision)
- [Recommender Systems](#recommender-systems)

**Web Development**

- [Web Frameworks](#web-frameworks)
- [Web APIs](#web-apis)
- [Web Servers](#web-servers)
- [WebSocket](#websocket)
- [Template Engines](#template-engines)
- [Web Asset Management](#web-asset-management)
- [Authentication](#authentication)
- [Admin Panels](#admin-panels)
- [CMS](#cms)
- [ERP](#erp)
- [Static Site Generators](#static-site-generators)

**HTTP & Scraping**

- [HTTP Clients](#http-clients)
- [Web Scraping](#web-scraping)
- [Email](#email)

**Database & Storage**

- [ORM](#orm)
- [Database Drivers](#database-drivers)
- [Database](#database)
- [Caching](#caching)
- [Search](#search)
- [Serialization](#serialization)

**Data & Science**

- [Data Analysis](#data-analysis)
- [Data Ingestion / ETL](#data-ingestion--etl)
- [Data Validation](#data-validation)
- [Data Visualization](#data-visualization)
- [Geolocation](#geolocation)
- [Science](#science)
- [Quantum Computing](#quantum-computing)

**Developer Tools**

- [Algorithms and Design Patterns](#algorithms-and-design-patterns)
- [Interactive Interpreter](#interactive-interpreter)
- [Code Analysis](#code-analysis)
- [Testing](#testing)
- [Debugging Tools](#debugging-tools)
- [Build Tools](#build-tools)
- [Documentation](#documentation)

**DevOps**

- [DevOps Tools](#devops-tools)
- [Distributed Computing](#distributed-computing)
- [Task Queues](#task-queues)
- [Messaging](#messaging)
- [Job Schedulers](#job-schedulers)
- [Logging](#logging)
- [Network Virtualization](#network-virtualization)

**CLI & GUI**

- [CLI Development](#cli-development)
- [CLI Tools](#cli-tools)
- [GUI Development](#gui-development)

**Text & Documents**

- [Text Processing](#text-processing)
- [HTML Manipulation](#html-manipulation)
- [File Format Processing](#file-format-processing)
- [File Manipulation](#file-manipulation)

**Media**

- [Image Processing](#image-processing)
- [Audio & Video Processing](#audio--video-processing)
- [Game Development](#game-development)

**Python Language**

- [Implementations](#implementations)
- [Built-in Classes Enhancement](#built-in-classes-enhancement)
- [Functional Programming](#functional-programming)
- [Asynchronous Programming](#asynchronous-programming)
- [Date and Time](#date-and-time)

**Python Toolchain**

- [Environment Management](#environment-management)
- [Package Management](#package-management)
- [Package Repositories](#package-repositories)
- [Distribution](#distribution)
- [Configuration Files](#configuration-files)

**Security**

- [Cryptography](#cryptography)
- [Penetration Testing](#penetration-testing)
- [Supply Chain Security](#supply-chain-security)
- [Web Security](#web-security)

**Other**

- [Hardware](#hardware)
- [Microsoft Windows](#microsoft-windows)
- [Miscellaneous](#miscellaneous)

## Projects

**AI & ML**

### AI and Agents

_Libraries for building AI applications, LLM integrations, and autonomous agents._

- Agent Skills
  - [django-ai-plugins](https://github.com/vintasoftware/django-ai-plugins) - Django backend agent skills for Django, DRF, Celery, and Django-specific code review.
  - [scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) - Agent skills for scientific research and analysis with Python libraries like scikit-learn, polars, and biopython.
  - [sentry-skills](https://github.com/getsentry/skills) - Agent skills the Sentry team uses for code review, pull requests, and Django reviews.
  - [trailofbits-skills](https://github.com/trailofbits/skills) - Security skills for vulnerability detection, auditing, and testing.
  - [wshobson-agents](https://github.com/wshobson/agents) - Plugins, agents, and skills for AI coding tools, including Python skills for testing, async, packaging, and uv.
- Orchestration
  - [langchain](https://github.com/langchain-ai/langchain) - A framework for building agents and LLM-powered applications.
  - [langgraph](https://github.com/langchain-ai/langgraph) - Low-level orchestration framework for building stateful, long-running LLM agents.
  - [pydantic-ai](https://github.com/pydantic/pydantic-ai) - A Python agent framework for building generative AI applications with structured schemas.
  - [crewai](https://github.com/crewAIInc/crewAI) - A framework for orchestrating role-playing autonomous AI agents for collaborative task solving.
- Vendor Agent SDKs
  - [claude-agent-sdk](https://github.com/anthropics/claude-agent-sdk-python) - Anthropic's Python SDK for building AI agents on Claude Code's harness — custom tools, in-process MCP servers, hooks.
  - [openai-agents](https://github.com/openai/openai-agents-python) - OpenAI's framework for building and managing AI agents.
  - [google-adk](https://github.com/google/adk-python) - Google's code-first toolkit for building, evaluating, and deploying AI agents.
- Model Context Protocol
  - [mcp](https://github.com/modelcontextprotocol/python-sdk) - The official Python SDK for building Model Context Protocol servers and clients.
  - [fastmcp](https://github.com/PrefectHQ/fastmcp) - A high-level, Pythonic framework for building MCP servers and clients.
- Personal Assistants
  - [hermes-agent](https://github.com/NousResearch/hermes-agent) - An adaptive personal AI assistant that grows with you.
  - [AstrBot](https://github.com/AstrBotDevs/AstrBot) - A multi-platform AI assistant that connects LLMs to chat apps like Telegram, Slack, and QQ, extensible with Python plugins.
- Prompt Optimization
  - [dspy](https://github.com/stanfordnlp/dspy) - A framework for programming, not prompting, language models.
- Data Layer
  - [instructor](https://github.com/567-labs/instructor) - A library for extracting structured data from LLMs, powered by Pydantic.
  - [llama-index](https://github.com/run-llama/llama_index) - A toolkit for building RAG pipelines and agents over your data.
  - [mem0](https://github.com/mem0ai/mem0) - An intelligent memory layer for AI agents enabling personalized interactions.
  - [openviking](https://github.com/volcengine/OpenViking) - A context database for AI agents that unifies memory, resources, and skills.
  - [semantica](https://github.com/semantica-agi/semantica) - A graph-native context and knowledge layer for AI agents with reasoning, provenance, and governance.
- Pre-trained Models
  - [transformers](https://github.com/huggingface/transformers) - The model-definition framework for pretrained models in text, computer vision, audio, video, and multimodal tasks, for inference and training.
  - [sentence-transformers](https://github.com/huggingface/sentence-transformers) - Compute embeddings, run retrieval, and rerank results with pretrained and fine-tuned models.
- Local LLM Inference
  - [ollama](https://github.com/ollama/ollama-python) - Python client for Ollama, which downloads and runs open-weight LLMs locally.
  - [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) - Python bindings for llama.cpp, for running GGUF models locally.
  - [mlx-lm](https://github.com/ml-explore/mlx-lm) - Run and fine-tune large language models on Apple Silicon with MLX.
- LLM Serving
  - [vllm](https://github.com/vllm-project/vllm) - A high-throughput and memory-efficient inference and serving engine for LLMs.
  - [sglang](https://github.com/sgl-project/sglang) - A high-performance serving framework for large language models and multimodal models.
  - [deepinfer](https://github.com/deepseek-ai/DeepInfer) - DeepSeek's production inference engine for DeepSeek models, with MoE expert parallelism.
- Image and Video Generation
  - [diffusers](https://github.com/huggingface/diffusers) - Pre-trained diffusion models for generating and editing images, audio, and video.
- Fine-tuning
  - [peft](https://github.com/huggingface/peft) - A library for parameter-efficient fine-tuning of large pretrained models.
  - [trl](https://github.com/huggingface/trl) - A library for post-training transformer language models with SFT, DPO, GRPO, and other trainers.
  - [unsloth](https://github.com/unslothai/unsloth) - Faster, lower-memory LLM fine-tuning, as a Python library or a desktop app.
  - [axolotl](https://github.com/axolotl-ai-cloud/axolotl) - A framework for fine-tuning and post-training large language models.
- Speech
  - [faster-whisper](https://github.com/SYSTRAN/faster-whisper) - A Whisper reimplementation on CTranslate2, up to 4 times faster than openai-whisper with less memory.
  - [openai-whisper](https://github.com/openai/whisper) - A general-purpose automatic speech recognition model trained on 680k hours of multilingual and multitask supervised data.
  - [gTTS](https://github.com/pndurette/gTTS) - Python library and CLI tool for converting text to speech using Google Translate TTS.
  - [funasr](https://github.com/modelscope/FunASR) - Industrial-grade speech recognition toolkit with speaker diarization and emotion detection.

### Deep Learning

_Frameworks for Neural Networks and Deep Learning. Also see [awesome-deep-learning](https://github.com/ChristosChristofidis/awesome-deep-learning)._

- Frameworks
  - [pytorch](https://github.com/pytorch/pytorch) - Tensors and Dynamic neural networks in Python with strong GPU acceleration.
  - [pytorch-lightning](https://github.com/Lightning-AI/pytorch-lightning) - Deep learning framework to train, deploy, and ship AI products Lightning fast.
  - [jax](https://github.com/jax-ml/jax) - A library for high-performance numerical computing with autodiff and JIT compilation.
  - [keras](https://github.com/keras-team/keras) - A high-level deep learning library with support for JAX, TensorFlow, and PyTorch backends.
  - [tensorflow](https://github.com/tensorflow/tensorflow) - An end-to-end machine learning platform from Google.
- Reinforcement Learning
  - [gymnasium](https://github.com/Farama-Foundation/Gymnasium) - A standard API for reinforcement learning environments with popular reference environments ([gym](https://github.com/openai/gym) successor).
  - [stable-baselines3](https://github.com/DLR-RM/stable-baselines3) - PyTorch implementations of Stable Baselines (deep) reinforcement learning algorithms.

### Machine Learning

_Libraries for Machine Learning. Also see [awesome-machine-learning](https://github.com/josephmisiti/awesome-machine-learning#python)._

- General
  - [scikit-learn](https://github.com/scikit-learn/scikit-learn) - The most popular Python library for Machine Learning with extensive documentation and community support.
  - [imbalanced-learn](https://github.com/scikit-learn-contrib/imbalanced-learn) - Resampling techniques for imbalanced datasets, compatible with scikit-learn.
  - [pgmpy](https://github.com/pgmpy/pgmpy) - A Python library for causal and probabilistic reasoning with graphical models.
  - [feature-engine](https://github.com/feature-engine/feature_engine) - sklearn compatible API with the widest toolset for feature engineering and selection.
- Gradient Boosting
  - [xgboost](https://github.com/dmlc/xgboost) - A scalable, portable, and distributed gradient boosting library.
  - [lightgbm](https://github.com/lightgbm-org/LightGBM) - A fast, distributed, high performance gradient boosting framework.
  - [catboost](https://github.com/catboost/catboost) - A fast, scalable, high performance gradient boosting on decision trees library.
- Time Series Forecasting
  - [prophet](https://github.com/facebook/prophet) - A tool for producing forecasts for time series with multiple seasonality and trend changes.
  - [statsforecast](https://github.com/Nixtla/statsforecast) - Fast statistical forecasting models such as ARIMA, ETS, and Theta, compiled with numba.
  - [sktime](https://github.com/sktime/sktime) - A unified scikit-learn-style framework for forecasting and other time-series learning tasks.
  - [timesfm](https://github.com/google-research/timesfm) - A pretrained foundation model from Google Research for time-series forecasting, with non-commercial default weights.
- Hyperparameter Optimization
  - [optuna](https://github.com/optuna/optuna) - A hyperparameter optimization framework with define-by-run search spaces and pruning of unpromising trials.
  - [hyperopt](https://github.com/hyperopt/hyperopt) - Distributed asynchronous hyperparameter optimization with Tree-structured Parzen Estimators.

### Natural Language Processing

_Libraries for working with human languages._

- General
  - [nltk](https://github.com/nltk/nltk) - A leading platform for building Python programs to work with human language data.
  - [spacy](https://github.com/explosion/spaCy) - A library for industrial-strength natural language processing in Python and Cython.
  - [gensim](https://github.com/piskvorky/gensim) - Topic Modeling for Humans.
  - [stanza](https://github.com/stanfordnlp/stanza) - The Stanford NLP Group's official Python library, supporting 60+ languages.
- Chinese
  - [jieba](https://github.com/fxsjy/jieba) - The most popular Chinese text segmentation library.
  - [pypinyin](https://github.com/mozillazg/python-pinyin) - Convert Chinese hanzi (漢字) to pinyin (拼音).
  - [OpenCC](https://github.com/BYVoid/OpenCC) - Traditional/Simplified Chinese conversion with regional variants and phrase-level rules.
  - [pangu.py](https://github.com/vinta/pangu.py) - Paranoid text spacing.

### Computer Vision

_Libraries for image and video analysis, object detection, and OCR._

- General
  - [opencv-python](https://github.com/opencv/opencv-python) - Open Source Computer Vision Library.
  - [ultralytics](https://github.com/ultralytics/ultralytics) - Ultralytics YOLO for object detection, segmentation, pose estimation, classification, and tracking.
  - [kornia](https://github.com/kornia/kornia) - Open Source Differentiable Computer Vision Library for PyTorch.
  - [fiftyone](https://github.com/voxel51/fiftyone) - The open-source tool for building high-quality datasets and computer vision models.
- OCR
  - [pytesseract](https://github.com/madmaze/pytesseract) - A wrapper for the [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) engine.
  - [easyocr](https://github.com/JaidedAI/EasyOCR) - Ready-to-use OCR with 80+ languages supported.
  - [paddleocr](https://github.com/PaddlePaddle/PaddleOCR) - Multilingual OCR and document parsing toolkit based on PaddlePaddle.

### Recommender Systems

_Libraries for building recommender systems._

- [annoy](https://github.com/spotify/annoy) - Approximate Nearest Neighbors in C++/Python optimized for memory usage.
- [implicit](https://github.com/benfred/implicit) - A fast Python implementation of collaborative filtering for implicit datasets.
- [scikit-surprise](https://github.com/NicolasHug/Surprise) - A scikit for building and analyzing recommender systems.

**Web Development**

### Web Frameworks

_Traditional full stack web frameworks. Also see [Web APIs](#web-apis)._

- Synchronous
  - [flask](https://github.com/pallets/flask) - A microframework for Python.
    - [awesome-flask](https://github.com/humiaozuzu/awesome-flask)
  - [django](https://github.com/django/django) - A high-level web framework that encourages rapid development and clean, pragmatic design.
    - [awesome-django](https://github.com/wsvincent/awesome-django)
  - [bottle](https://github.com/bottlepy/bottle) - A fast and simple micro-framework distributed as a single file with no dependencies.
  - [pyramid](https://github.com/Pylons/pyramid) - A small, fast, down-to-earth, open source Python web framework.
  - [fasthtml](https://github.com/AnswerDotAI/fasthtml) - The fastest way to create an HTML app.
- Asynchronous
  - [starlette](https://github.com/Kludex/starlette) - A lightweight ASGI framework and toolkit for building high-performance async services.
  - [tornado](https://github.com/tornadoweb/tornado) - A web framework and asynchronous networking library.
  - [litestar](https://github.com/litestar-org/litestar) - Production-ready, capable and extensible ASGI Web framework.
  - [reflex](https://github.com/reflex-dev/reflex) - A framework for building reactive, full-stack web applications entirely with Python.

### Web APIs

_Libraries for building RESTful, GraphQL, and RPC APIs._

- Django
  - [django-rest-framework](https://github.com/encode/django-rest-framework) - A powerful and flexible toolkit to build web APIs.
  - [django-ninja](https://github.com/vitalik/django-ninja) - Fast, Django REST framework based on type hints and Pydantic.
  - [strawberry-django](https://github.com/strawberry-graphql/strawberry-django) - Strawberry GraphQL integration with Django.
  - [django-modern-rest](https://github.com/wemake-services/django-modern-rest) - Modern REST with speed, types, async, `msgspec`, `pydantic` and other goodies.
- Flask
  - [flask-restx](https://github.com/python-restx/flask-restx) - Fully featured framework for fast, easy and documented API development with Flask.
  - [flask-smorest](https://github.com/marshmallow-code/flask-smorest) - A Flask/Marshmallow-based REST API framework with automatic OpenAPI documentation.
  - [apiflask](https://github.com/apiflask/apiflask) - A lightweight Python web API framework based on Flask, supporting marshmallow schemas and Pydantic models.
- Framework Agnostic
  - [fastapi](https://github.com/fastapi/fastapi) - A modern, fast, web framework for building APIs with standard Python type hints.
  - [strawberry](https://github.com/strawberry-graphql/strawberry) - A GraphQL library that leverages Python type annotations for schema definition.
  - [connexion](https://github.com/spec-first/connexion) - A spec-first framework that handles requests based on your OpenAPI specification.
- RPC
  - [grpcio](https://github.com/grpc/grpc) - HTTP/2-based RPC framework with Python bindings, built by Google.

### Web Servers

_ASGI and WSGI compatible web servers._

- ASGI
  - [uvicorn](https://github.com/Kludex/uvicorn) - A lightning-fast ASGI server implementation.
  - [granian](https://github.com/emmett-framework/granian) - A Rust HTTP server for Python apps built on Hyper and Tokio, supporting WSGI/ASGI/RSGI.
  - [hypercorn](https://github.com/pgjones/hypercorn) - An ASGI and WSGI Server based on Hyper libraries and inspired by Gunicorn.
- WSGI
  - [gunicorn](https://github.com/benoitc/gunicorn) - A pre-fork WSGI server with a native ASGI worker, ported from Ruby's Unicorn project.
  - [waitress](https://github.com/Pylons/waitress) - Multi-threaded, powers Pyramid.

### WebSocket

_Libraries for working with WebSocket._

- [websockets](https://github.com/python-websockets/websockets) - A library for building WebSocket servers and clients with a focus on correctness and simplicity.
- [channels](https://github.com/django/channels) - Brings WebSocket, long-poll HTTP, and other async support to Django.
- [flask-socketio](https://github.com/miguelgrinberg/Flask-SocketIO) - Socket.IO integration for Flask applications.
- [autobahn-python](https://github.com/crossbario/autobahn-python) - WebSocket & WAMP for Python on Twisted and [asyncio](https://docs.python.org/3/library/asyncio.html).

### Template Engines

_Libraries for rendering text and HTML from templates._

- [jinja](https://github.com/pallets/jinja) - A modern and designer friendly templating language.
- [mako](https://github.com/sqlalchemy/mako) - Hyperfast and lightweight templating for the Python platform.

### Web Asset Management

_Tools for managing, storing, compressing and minifying website assets._

- [whitenoise](https://github.com/evansd/whitenoise) - Simplified static file serving for WSGI apps, with compression and caching headers.
- [django-storages](https://github.com/jschneier/django-storages) - A collection of custom storage back ends for Django.
- [django-compressor](https://github.com/django-compressor/django-compressor) - Compresses linked and inline JavaScript or CSS into a single cached file.

### Authentication

_Libraries for implementing authentication schemes._

- OAuth
  - [oauthlib](https://github.com/oauthlib/oauthlib) - A generic and thorough implementation of the OAuth request-signing logic.
  - [authlib](https://github.com/authlib/authlib) - A comprehensive library for building OAuth, OpenID Connect, and JWT/JWS/JWE/JWK/JWA.
  - [django-allauth](https://github.com/pennersr/django-allauth) - Authentication app for Django that "just works."
  - [django-oauth-toolkit](https://github.com/django-oauth/django-oauth-toolkit) - An OAuth 2.0 authorization server for Django.
- JWT
  - [pyjwt](https://github.com/jpadilla/pyjwt) - JSON Web Token implementation in Python.
- Permissions
  - [django-guardian](https://github.com/django-guardian/django-guardian) - Implementation of per-object permissions for Django.
  - [django-rules](https://github.com/dfunckt/django-rules) - A tiny but powerful app for object-level permissions in Django, without a database.

### Admin Panels

_Libraries for administrative interfaces._

- [flask-admin](https://github.com/pallets-eco/flask-admin) - Simple and extensible administrative interface framework for Flask.
- [django-unfold](https://github.com/unfoldadmin/django-unfold) - A modern Django admin theme for building dashboards, internal tools, and business applications.
- [sqladmin](https://github.com/smithyhq/sqladmin) - An admin interface for SQLAlchemy models in FastAPI and Starlette.
- [django-grappelli](https://github.com/sehmaschine/django-grappelli) - A jazzy skin for the Django Admin-Interface.

### CMS

_Content Management Systems._

- [wagtail](https://github.com/wagtail/wagtail) - A Django content management system.
- [django-cms](https://github.com/django-cms/django-cms) - The easy-to-use and developer-friendly enterprise CMS powered by Django.

### ERP

_Enterprise resource planning frameworks._

- [odoo](https://github.com/odoo/odoo) - A suite of open source business apps: CRM, e-commerce, accounting, inventory, and thousands of community modules.

### Static Site Generators

_Static site generator is a software that takes some text + templates as input and produces HTML files on the output._

- [pelican](https://github.com/getpelican/pelican) - Static site generator that supports Markdown and reST syntax.
- [nikola](https://github.com/getnikola/nikola) - A static website and blog generator.

**HTTP & Scraping**

### HTTP Clients

_Libraries for working with HTTP._

- General
  - [requests](https://github.com/psf/requests) - HTTP Requests for Humans.
  - [aiohttp](https://github.com/aio-libs/aiohttp) - Asynchronous HTTP client/server framework for asyncio and Python.
  - [httpx2](https://github.com/pydantic/httpx2) - HTTP/1.1 and HTTP/2 client with sync and async APIs, maintained by Pydantic ([httpx](https://github.com/encode/httpx) fork).
  - [urllib3](https://github.com/urllib3/urllib3) - An HTTP library with thread-safe connection pooling, file post, and more.
  - [httpx](https://github.com/encode/httpx) - A next generation HTTP client for Python.
- URL Manipulation
  - [yarl](https://github.com/aio-libs/yarl) - Yet another URL library.

### Web Scraping

_Libraries to automate web scraping and extract web content._

- Frameworks
  - [browser-use](https://github.com/browser-use/browser-use) - Make websites accessible for AI agents with easy browser automation.
  - [scrapy](https://github.com/scrapy/scrapy) - A fast high-level web crawling and scraping framework.
  - [crawl4ai](https://github.com/unclecode/crawl4ai) - An open-source, LLM-friendly web crawler that provides lightning-fast, structured data extraction specifically designed for AI agents.
  - [stagehand](https://github.com/browserbase/stagehand) - A fast and token-efficient browser automation SDK to extract data and perform self-healing actions on web pages.
  - [scrapling](https://github.com/D4Vinci/Scrapling) - An adaptive scraping framework whose selectors relocate elements after page changes, with stealth fetchers and spiders.
- Content Extraction
  - [markdownify](https://github.com/matthewwithanm/python-markdownify) - Convert HTML to Markdown, with customizable tag handling.
  - [feedparser](https://github.com/kurtmckee/feedparser) - Universal feed parser.
  - [trafilatura](https://github.com/adbar/trafilatura) - A tool for gathering text and metadata from the web, with built-in content filtering.

### Email

_Libraries for sending email._

- [aiosmtplib](https://github.com/cole/aiosmtplib) - An asyncio SMTP client.
- [django-anymail](https://github.com/anymail/django-anymail) - Django email backends and webhooks for transactional email services such as Amazon SES, Brevo, Mailgun, Postmark, and Resend.
- [yagmail](https://github.com/kootenpv/yagmail) - Yet another Gmail/SMTP client.

**Database & Storage**

### ORM

_Libraries that implement Object-Relational Mapping or data mapping techniques._

- Relational Databases
  - [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy) - The Python SQL Toolkit and Object Relational Mapper.
    - [awesome-sqlalchemy](https://github.com/dahlia/awesome-sqlalchemy)
  - [django.db.models](https://github.com/django/django) - (part of Django) The Django [ORM](https://docs.djangoproject.com/en/stable/topics/db/models/).
  - [peewee](https://github.com/coleifer/peewee) - A small, expressive ORM.
  - [sqlmodel](https://github.com/fastapi/sqlmodel) - SQLModel is based on Python type annotations, and powered by Pydantic and SQLAlchemy.
- NoSQL Databases
  - [pynamodb](https://github.com/pynamodb/PynamoDB) - A Pythonic interface for [Amazon DynamoDB](https://aws.amazon.com/dynamodb/).
  - [mongoengine](https://github.com/MongoEngine/mongoengine) - A Python Object-Document-Mapper for working with MongoDB.
  - [beanie](https://github.com/BeanieODM/beanie) - An asynchronous Python object-document mapper (ODM) for MongoDB.
  - [django-mongodb-backend](https://github.com/mongodb/django-mongodb-backend) - Official MongoDB database backend for Django.

### Database Drivers

_Libraries for connecting and operating databases._

- MySQL - [awesome-mysql](https://github.com/shlomi-noach/awesome-mysql)
  - [pymysql](https://github.com/PyMySQL/PyMySQL) - A pure-Python MySQL and MariaDB client library, based on PEP 249.
  - [mysqlclient](https://github.com/PyMySQL/mysqlclient) - MySQL and MariaDB connector ([MySQLdb1](https://github.com/farcepest/MySQLdb1) fork).
- PostgreSQL - [awesome-postgres](https://github.com/dhamaniasad/awesome-postgres)
  - [psycopg](https://github.com/psycopg/psycopg) - A PostgreSQL adapter for Python, the successor to psycopg2.
  - [asyncpg](https://github.com/MagicStack/asyncpg) - A fast PostgreSQL Database Client Library for Python/asyncio.
  - [pgvector](https://github.com/pgvector/pgvector-python) - pgvector support for Python, adding vector types and similarity search to psycopg, asyncpg, SQLAlchemy, and Django.
- SQLite - [awesome-sqlite](https://github.com/planetopendata/awesome-sqlite)
  - [sqlite3](https://docs.python.org/3/library/sqlite3.html) - (Python standard library) SQLite interface compliant with DB-API 2.0.
  - [apsw](https://github.com/rogerbinns/apsw) - Another Python SQLite Wrapper, exposing the complete SQLite C API.
  - [sqlite-utils](https://github.com/simonw/sqlite-utils) - Python CLI utility and library for manipulating SQLite databases.
- ClickHouse
  - [clickhouse-connect](https://github.com/ClickHouse/clickhouse-connect) - The official ClickHouse client, with SQLAlchemy and Superset connectors.
  - [clickhouse-driver](https://github.com/mymarilyn/clickhouse-driver) - Python driver with native interface for ClickHouse.
- Other Relational Databases
  - [pyodbc](https://github.com/mkleehammer/pyodbc) - An ODBC bridge for connecting to SQL Server and any other ODBC-accessible database.
  - [oracledb](https://github.com/oracle/python-oracledb) - The official Python driver for Oracle Database, successor to cx_Oracle.
  - [mssql-python](https://github.com/microsoft/mssql-python) - Official Microsoft driver for SQL Server and Azure SQL, built on ODBC for high performance.
- NoSQL Databases
  - [redis](https://github.com/redis/redis-py) - The Python client for Redis.
  - [pymongo](https://github.com/mongodb/mongo-python-driver) - The official Python client for MongoDB.
  - [cassandra-driver](https://github.com/apache/cassandra-python-driver) - The Python Driver for Apache Cassandra.

### Database

_In-process databases usable directly from Python._

- Analytical
  - [duckdb](https://github.com/duckdb/duckdb) - An in-process SQL OLAP database management system; optimized for analytics and fast queries, similar to SQLite but for analytical workloads.
  - [chdb](https://github.com/chdb-io/chdb) - In-process OLAP SQL engine with the full ClickHouse dialect, zero-copy pandas/Arrow interop, and federation to remote ClickHouse clusters via `remoteSecure()`.
- Vector
  - [lancedb](https://github.com/lancedb/lancedb) - A developer-friendly embedded retrieval database for multimodal AI.
  - [chromadb](https://github.com/chroma-core/chroma) - An open-source embedding database for building AI applications with semantic search.
  - [zvec](https://github.com/alibaba/zvec) - A lightweight, in-process vector database that embeds directly into applications.
- Key-Value & Document
  - [tinydb](https://github.com/msiemens/tinydb) - A tiny, document-oriented database.

### Caching

_Libraries for caching data._

- General
  - [cachetools](https://github.com/tkem/cachetools) - Extensible memoizing collections and decorators.
  - [diskcache](https://github.com/grantjenks/python-diskcache) - SQLite and file backed cache backend, compatible with Django.
  - [dogpile.cache](https://github.com/sqlalchemy/dogpile.cache) - A caching API for Redis, Memcached, and others, with coordinated value regeneration.
- HTTP Responses
  - [hishel](https://github.com/karpetrosyan/hishel) - RFC 9111 compliant HTTP caching for clients like httpx and requests and servers like FastAPI, with sync and async support.
- Django
  - [django-redis](https://github.com/jazzband/django-redis) - Full-featured Redis cache backend for Django.
  - [django-cacheops](https://github.com/Suor/django-cacheops) - A slick ORM cache with automatic granular event-driven invalidation.

### Search

_Libraries and software for indexing and performing search queries on data._

- Full-Text Search
  - [opensearch-py](https://github.com/opensearch-project/opensearch-py) - The official low-level Python client for [OpenSearch](https://opensearch.org/).
  - [elasticsearch](https://github.com/elastic/elasticsearch-py) - The official low-level Python client for [Elasticsearch](https://www.elastic.co/elasticsearch).
  - [meilisearch](https://github.com/meilisearch/meilisearch-python) - The official Python client for the [Meilisearch](https://www.meilisearch.com/) search engine.
  - [django-haystack](https://github.com/django-haystack/django-haystack) - Modular search for Django.
- Vector Search
  - [faiss-cpu](https://github.com/facebookresearch/faiss) - A library for efficient similarity search and clustering of dense vectors.

### Serialization

_Libraries for serializing complex data types._

- Data Formats
  - [msgpack](https://github.com/msgpack/msgpack-python) - MessagePack serializer implementation for Python.
  - [orjson](https://github.com/ijl/orjson) - Fast, correct JSON library.
  - [marshmallow](https://github.com/marshmallow-code/marshmallow) - A lightweight library for converting complex objects to and from simple Python datatypes.
  - [msgspec](https://github.com/msgspec/msgspec) - A fast serialization and validation library supporting JSON, MessagePack, YAML, and TOML.
- Object Pickling
  - [cloudpickle](https://github.com/cloudpipe/cloudpickle) - Extends pickle to functions, lambdas, and interactively defined classes, for shipping code to remote workers.
  - [dill](https://github.com/uqfoundation/dill) - Extends pickle to serialize almost any object, including closures and interpreter sessions.

**Data & Science**

### Data Analysis

_Libraries for data analysis._

- [pandas](https://github.com/pandas-dev/pandas) - A library providing high-performance, easy-to-use data structures and data analysis tools.
- [polars](https://github.com/pola-rs/polars) - A fast DataFrame library implemented in Rust with a Python API.
- [ibis-framework](https://github.com/ibis-project/ibis) - A portable Python dataframe library with a single API for 20+ backends.

### Data Ingestion / ETL

_Libraries for data extraction, transformation, and loading pipelines across multiple sources and destinations._

- General
  - [awswrangler](https://github.com/aws/aws-sdk-pandas) - Pandas integration with AWS services like Athena, Glue, Redshift, S3, and DynamoDB.
  - [dlt](https://github.com/dlt-hub/dlt) - A Python library for building data pipelines with automatic schema inference, incremental loading, and support for multiple sources and destinations.
- Financial Data
  - [yfinance](https://github.com/ranaroussi/yfinance) - Easy Pythonic way to download market and financial data from Yahoo Finance.
  - [akshare](https://github.com/akfamily/akshare) - A financial data interface library, with data provided for academic research only.
  - [edgartools](https://github.com/dgunning/edgartools) - Downloads SEC EDGAR filings and XBRL financial statements as structured data.
  - [openbb](https://github.com/openbq-org/OpenBB) - A financial data platform for analysts, quants and AI agents.

### Data Validation

_Libraries for validating data._

- [pydantic](https://github.com/pydantic/pydantic) - Data validation using Python type hints.
- [jsonschema](https://github.com/python-jsonschema/jsonschema) - An implementation of [JSON Schema](https://json-schema.org/) for Python.
- [great-expectations](https://github.com/fivetran/great_expectations) - A data quality framework for validating, documenting, and profiling data with declarative expectations.
- [pandera](https://github.com/unionai-oss/pandera) - A data validation library for dataframes, with support for pandas, polars, PySpark, and more.

### Data Visualization

_Libraries for visualizing data. Also see [awesome-javascript](https://github.com/sorrycc/awesome-javascript#data-visualization)._

- Plotting
  - [matplotlib](https://github.com/matplotlib/matplotlib) - A comprehensive library for creating static, animated, and interactive visualizations.
  - [plotly](https://github.com/plotly/plotly.py) - Interactive graphing library for Python.
  - [seaborn](https://github.com/mwaskom/seaborn) - Statistical data visualization using Matplotlib.
  - [altair](https://github.com/vega/altair) - Declarative statistical visualization library for Python.
  - [bokeh](https://github.com/bokeh/bokeh) - Interactive Web Plotting for Python.
- Specialized
  - [graphviz](https://github.com/xflr6/graphviz) - Simple Python interface for creating and rendering Graphviz graphs.
  - [cartopy](https://github.com/SciTools/cartopy) - A cartographic Python library with matplotlib support.
  - [graphify](https://github.com/Graphify-Labs/graphify) - Turns code, SQL schemas, docs, papers, images, or videos into a queryable knowledge graph.
- Dashboards and Apps
  - [streamlit](https://github.com/streamlit/streamlit) - A framework which lets you build dashboards, generate reports, or create chat apps in minutes.
  - [dash](https://github.com/plotly/dash) - A framework for building data apps and dashboards in pure Python, built on Plotly.
  - [gradio](https://github.com/gradio-app/gradio) - Build and share machine learning apps, all in Python.

### Geolocation

_Libraries for geocoding addresses and working with latitudes and longitudes._

- [geopandas](https://github.com/geopandas/geopandas) - Python tools for geographic data (GeoSeries/GeoDataFrame) built on pandas.
- [geopy](https://github.com/geopy/geopy) - Python Geocoding Toolbox.
- [geojson](https://github.com/jazzband/geojson) - Python bindings and utilities for GeoJSON.
- [geodjango](https://github.com/django/django) - (part of Django) A world-class [geographic web framework](https://docs.djangoproject.com/en/stable/ref/contrib/gis/).

### Science

_Libraries for scientific computing. Also see [Python-for-Scientists](https://github.com/TomNicholas/Python-for-Scientists)._

- Core
  - [numpy](https://github.com/numpy/numpy) - A fundamental package for scientific computing with Python.
  - [scipy](https://github.com/scipy/scipy) - Fundamental algorithms for scientific computing in Python.
  - [numba](https://github.com/numba/numba) - A NumPy-aware JIT compiler for Python, using LLVM.
- Symbolic Mathematics
  - [sympy](https://github.com/sympy/sympy) - A Python library for symbolic mathematics.
- Statistics
  - [statsmodels](https://github.com/statsmodels/statsmodels) - Statistical modeling and econometrics in Python.
- Biology and Chemistry
  - [rdkit](https://github.com/rdkit/rdkit) - Cheminformatics and Machine Learning Software.
  - [biopython](https://github.com/biopython/biopython) - Biopython is a set of freely available tools for biological computation.
- Physics and Engineering
  - [pint](https://github.com/hgrecco/pint) - Operate and manipulate physical quantities with units and dimensional analysis.
  - [astropy](https://github.com/astropy/astropy) - A community Python library for Astronomy.
  - [obspy](https://github.com/obspy/obspy) - A Python toolbox for seismology.
- Simulation and Modeling
  - [pymc](https://github.com/pymc-devs/pymc) - Probabilistic programming and Bayesian modeling in Python.
  - [simpy](https://gitlab.com/team-simpy/simpy) - A process-based discrete-event simulation framework.
  - [mesa](https://github.com/mesa/mesa) - An agent-based modeling framework for building, analyzing, and visualizing complex system simulations.
- Graphs and Networks
  - [networkx](https://github.com/networkx/networkx) - A high-productivity software for complex networks.
- Computational Geometry
  - [shapely](https://github.com/shapely/shapely) - Manipulation and analysis of geometric objects in the Cartesian plane.
- Other
  - [colour-science](https://github.com/colour-science/colour) - Implementing a comprehensive number of colour theory transformations and algorithms.
  - [manim](https://github.com/ManimCommunity/manim) - An animation engine for explanatory math videos.

### Quantum Computing

_Libraries for quantum computing._

- [qiskit](https://github.com/Qiskit/qiskit) - An IBM-backed quantum SDK for building, simulating, and running circuits on real quantum hardware.
- [qutip](https://github.com/qutip/qutip) - Quantum Toolbox in Python.
- [pennylane](https://github.com/PennyLaneAI/pennylane) - A cross-platform library for quantum computing, quantum ML, and quantum chemistry.
- [cirq](https://github.com/quantumlib/Cirq) - A Google-developed framework focused on hardware-aware quantum circuit design for NISQ devices.

**Developer Tools**

### Algorithms and Design Patterns

_Python implementation of data structures, algorithms and design patterns. Also see [awesome-algorithms](https://github.com/tayllan/awesome-algorithms)._

- Algorithms
  - [sortedcontainers](https://github.com/grantjenks/python-sortedcontainers) - Fast and pure-Python implementation of sorted collections.
  - [algorithms](https://github.com/keon/algorithms) - Minimal examples of data structures and algorithms.
  - [thealgorithms](https://github.com/TheAlgorithms/Python) - All Algorithms implemented in Python.
- Design Patterns
  - [python-patterns](https://github.com/faif/python-patterns) - A collection of design patterns and idioms in Python.
  - [python-statemachine](https://github.com/fgmacedo/python-statemachine) - Expressive statecharts and finite state machines with a declarative API, in sync and async codebases.

### Interactive Interpreter

_Interactive Python interpreters (REPL)._

- [ipython](https://github.com/ipython/ipython) - A powerful interactive Python shell, and the kernel behind Jupyter notebooks.
- [notebook](https://github.com/jupyter/notebook) - A web-based notebook environment for interactive computing.
  - [awesome-jupyter](https://github.com/markusschanta/awesome-jupyter)
- [marimo](https://github.com/marimo-team/marimo) - A reactive notebook for Python, stored as pure Python and runnable as a script or app.
- [ptpython](https://github.com/prompt-toolkit/ptpython) - Advanced Python REPL built on top of the [python-prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit).

### Code Analysis

_Tools of static analysis, linters and code quality checkers. Also see [awesome-static-analysis](https://github.com/analysis-tools-dev/static-analysis)._

- General
  - [import-linter](https://github.com/seddonym/import-linter) - A linter that enforces architectural constraints on imports between Python modules.
  - [vulture](https://github.com/jendrikseipp/vulture) - A tool for finding and analyzing dead Python code.
  - [complexipy](https://github.com/rohaquinlop/complexipy) - Cognitive complexity analysis for Python code, written in Rust.
  - [prospector](https://github.com/prospector-dev/prospector) - A tool to analyze Python code.
- Git Hooks
  - [pre-commit](https://github.com/pre-commit/pre-commit) - A framework for managing and maintaining multi-language pre-commit hooks.
- Linters and Formatters
  - [ruff](https://github.com/astral-sh/ruff) - An extremely fast Python linter and code formatter.
  - [black](https://github.com/psf/black) - The uncompromising Python code formatter.
  - [isort](https://github.com/PyCQA/isort) - A Python utility / library to sort imports.
  - [pylint](https://github.com/pylint-dev/pylint) - A fully customizable source code analyzer.
  - [flake8](https://github.com/PyCQA/flake8) - A wrapper around `pycodestyle`, `pyflakes` and McCabe.
    - [awesome-flake8-extensions](https://github.com/DmytroLitvinov/awesome-flake8-extensions)
  - [bandit](https://github.com/PyCQA/bandit) - A tool designed to find common security issues in Python code.
- Refactoring
  - [rope](https://github.com/python-rope/rope) - Rope is a Python refactoring library.
  - [ast-grep-cli](https://github.com/ast-grep/ast-grep) - A CLI tool for structural code search, linting, and rewriting based on syntax trees.
- Type Checkers - [awesome-python-typing](https://github.com/typeddjango/awesome-python-typing)
  - [mypy](https://github.com/python/mypy) - A static type checker for Python.
  - [ty](https://github.com/astral-sh/ty) - An extremely fast Python type checker and language server.
  - [pyright](https://github.com/microsoft/pyright) - Full-featured static type checker for Python from Microsoft, the engine behind Pylance.
  - [pyrefly](https://github.com/facebook/pyrefly) - A fast type checker and language server for Python.

### Testing

_Libraries for testing codebases and generating test data. Also see [awesome-python-testing](https://github.com/cleder/awesome-python-testing)._

- Frameworks
  - [pytest](https://github.com/pytest-dev/pytest) - A mature full-featured Python testing tool.
    - [awesome-pytest](https://github.com/augustogoulart/awesome-pytest)
  - [hypothesis](https://github.com/HypothesisWorks/hypothesis) - Hypothesis is an advanced Quickcheck style property based testing library.
  - [robotframework](https://github.com/robotframework/robotframework) - A generic test automation framework.
- Test Runners
  - [tox](https://github.com/tox-dev/tox) - Auto builds and tests distributions in multiple Python versions.
  - [nox](https://github.com/wntrblm/nox) - Flexible test automation for Python.
- Browser Automation
  - [playwright-python](https://github.com/microsoft/playwright-python) - Python version of the Playwright testing and automation library.
  - [selenium](https://github.com/SeleniumHQ/selenium) - Python bindings for [Selenium](https://selenium.dev/) [WebDriver](https://selenium.dev/documentation/webdriver/).
  - [seleniumbase](https://github.com/seleniumbase/SeleniumBase) - Python framework for web automation & testing, with stealth options.
- Load Testing
  - [locust](https://github.com/locustio/locust) - Scalable user load testing tool written in Python.
- API Testing
  - [schemathesis](https://github.com/schemathesis/schemathesis) - Automatic property-based testing of web APIs from OpenAPI or GraphQL schemas.
- Mock
  - [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) - (Python standard library) A mocking and patching library.
  - [responses](https://github.com/getsentry/responses) - A utility library for mocking out the requests Python library.
  - [vcrpy](https://github.com/kevin1024/vcrpy) - Record and replay HTTP interactions on your tests.
  - [respx](https://github.com/lundberg/respx) - Mock HTTPX with awesome request patterns and response side effects.
  - [time-machine](https://github.com/adamchainz/time-machine) - Travel through time in your tests by mocking the current time at the C level.
- Object Factories
  - [factory-boy](https://github.com/FactoryBoy/factory_boy) - A test fixtures replacement for Python.
  - [polyfactory](https://github.com/litestar-org/polyfactory) - A mock data generation library based on type hints (continuation of `pydantic-factories`).
- Code Coverage
  - [coverage](https://github.com/coveragepy/coveragepy) - Code coverage measurement.
- Fake Data
  - [faker](https://github.com/joke2k/faker) - A Python package that generates fake data.
  - [mimesis](https://github.com/lk-geimfari/mimesis) - A Python library for generating fake but realistic data in multiple languages and locales.

### Debugging Tools

_Libraries for debugging code._

- pdb-like Debugger
  - [ipdb](https://github.com/gotcha/ipdb) - IPython-enabled [pdb](https://docs.python.org/3/library/pdb.html).
  - [pudb](https://github.com/inducer/pudb) - A full-screen, console-based Python debugger.
- Tracing
  - [viztracer](https://github.com/gaogaotiantian/viztracer) - A low-overhead tool that traces and visualizes Python code execution.
- Profiler
  - [py-spy](https://github.com/benfred/py-spy) - A sampling profiler for Python programs. Written in Rust.
  - [memray](https://github.com/bloomberg/memray) - Tracks memory allocations in Python code, native extensions, and the interpreter itself.
  - [pyinstrument](https://github.com/joerick/pyinstrument) - A statistical wall-clock profiler with low overhead and readable call-tree output.
  - [scalene](https://github.com/plasma-umass/scalene) - A high-performance, high-precision CPU, GPU, and memory profiler for Python.
- Others
  - [django-debug-toolbar](https://github.com/django-commons/django-debug-toolbar) - Display various debug information for Django.
  - [django-silk](https://github.com/jazzband/django-silk) - Live profiling and inspection of HTTP requests and database queries for Django.
  - [icecream](https://github.com/gruns/icecream) - Inspect variables, expressions, and program execution with a single, simple function call.
  - [flask-debugtoolbar](https://github.com/pallets-eco/flask-debugtoolbar) - A port of the django-debug-toolbar to flask.

### Build Tools

_Task runners and software build tools. If you're looking for Python packaging/build tools, see [Package Management](#package-management)._

- [invoke](https://github.com/pyinvoke/invoke) - A tool for managing shell-oriented subprocesses and organizing executable Python code into CLI-invokable tasks.
- [poethepoet](https://github.com/nat-n/poethepoet) - A task runner that defines tasks in pyproject.toml and works with poetry or uv.
- [scons](https://github.com/SCons/scons) - A software construction tool.
- [doit](https://github.com/pydoit/doit) - A task runner and build tool.

### Documentation

_Libraries for generating project documentation._

- [sphinx](https://github.com/sphinx-doc/sphinx) - Python Documentation generator.
  - [awesome-sphinxdoc](https://github.com/ygzgxyz/awesome-sphinxdoc)
- [mkdocs-material](https://github.com/squidfunk/mkdocs-material) - A documentation framework and Material Design theme built on MkDocs.
- [diagrams](https://github.com/mingrammer/diagrams) - Diagram as Code.
- [pdoc](https://github.com/mitmproxy/pdoc) - Auto-generates API documentation for Python projects.
- [zensical](https://github.com/zensical/zensical) - A modern static site generator for technical documentation.

**DevOps**

### DevOps Tools

_Software and libraries for DevOps._

- Cloud Providers
  - [boto3](https://github.com/boto/boto3) - Python interface to Amazon Web Services.
  - [awscli](https://github.com/aws/aws-cli) - Universal Command Line Interface for Amazon Web Services; the PyPI package is v1, in maintenance mode, while v2 ships as AWS's bundled installer.
  - [azure-sdk-for-python](https://github.com/Azure/azure-sdk-for-python) - Microsoft Azure SDK for Python, published as per-service packages.
  - [google-cloud-python](https://github.com/googleapis/google-cloud-python) - Google Cloud client libraries for Python, published as per-service packages.
- Configuration Management
  - [ansible](https://github.com/ansible/ansible) - A radically simple IT automation platform.
  - [cloud-init](https://github.com/canonical/cloud-init) - A multi-distribution package that handles early initialization of a cloud instance.
  - [pyinfra](https://github.com/pyinfra-dev/pyinfra) - Turns Python code into shell commands and runs them on your servers.
  - [salt](https://github.com/saltstack/salt) - Infrastructure automation and management system.
- Deployment
  - [fabric](https://github.com/fabric/fabric) - A simple, Pythonic tool for remote execution and deployment.
  - [chalice](https://github.com/aws/chalice) - A Python serverless microframework for AWS.
- Monitoring and Processes
  - [psutil](https://github.com/giampaolo/psutil) - A cross-platform process and system utilities module.
  - [sentry-sdk](https://github.com/getsentry/sentry-python) - Sentry SDK for Python.
  - [supervisor](https://github.com/Supervisor/supervisor) - Supervisor process control system for UNIX.
  - [flower](https://github.com/mher/flower) - A real-time monitor and web admin for Celery task queues.
  - [sh](https://github.com/amoffat/sh) - A full-fledged subprocess replacement for Python.
- Other
  - [borgbackup](https://github.com/borgbackup/borg) - A deduplicating archiver with compression and encryption.

### Distributed Computing

_Frameworks and libraries for Distributed Computing._

- [pyspark](https://github.com/apache/spark) - [Apache Spark](https://spark.apache.org/) Python API.
- [dask](https://github.com/dask/dask) - A flexible parallel computing library for analytic computing.
- [ray](https://github.com/ray-project/ray) - A unified framework for scaling AI and Python applications.
- [joblib](https://github.com/joblib/joblib) - Parallel computing and disk-based caching for Python functions.
- [mpi4py](https://github.com/mpi4py/mpi4py) - Python bindings for MPI.

### Task Queues

_Libraries for working with task queues._

- [celery](https://github.com/celery/celery) - An asynchronous task queue/job queue based on distributed message passing.
- [rq](https://github.com/rq/rq) - Simple job queues for Python.
- [dramatiq](https://github.com/Bogdanp/dramatiq) - A fast and reliable background task processing library for Python 3.
- [huey](https://github.com/coleifer/huey) - A little task queue with multi-process, multi-thread, or greenlet workers.
- [taskiq](https://github.com/taskiq-python/taskiq) - Distributed task queue with native asyncio support and pluggable brokers.

### Messaging

_Libraries for working with message brokers and event streaming._

- [confluent-kafka](https://github.com/confluentinc/confluent-kafka-python) - Confluent's Python client for Apache Kafka, built on librdkafka.
- [pika](https://github.com/pika/pika) - Pure-Python RabbitMQ/AMQP 0-9-1 client library.
- [paho-mqtt](https://github.com/eclipse-paho/paho.mqtt.python) - The Eclipse Paho MQTT client for Python.
- [faststream](https://github.com/ag2ai/faststream) - A framework for building async services over Kafka, RabbitMQ, NATS, MQTT, and Redis.

### Job Schedulers

_Libraries for scheduling jobs._

- Task Scheduling
  - [apscheduler](https://github.com/agronholm/apscheduler) - A light but powerful in-process task scheduler that lets you schedule functions.
  - [schedule](https://github.com/dbader/schedule) - Python job scheduling for humans.
- Workflow Orchestration
  - [temporalio](https://github.com/temporalio/sdk-python) - Temporal SDK for durable, fault-tolerant workflows that survive crashes and retries.
  - [dagster](https://github.com/dagster-io/dagster) - An orchestration platform for the development, production, and observation of data assets.
  - [apache-airflow](https://github.com/apache/airflow) - Airflow is a platform to programmatically author, schedule and monitor workflows.
  - [prefect](https://github.com/PrefectHQ/prefect) - A modern workflow orchestration framework that makes it easy to build, schedule and monitor robust data pipelines.

### Logging

_Libraries for generating and working with logs._

- [logging](https://docs.python.org/3/library/logging.html) - (Python standard library) Logging facility for Python.
- [structlog](https://github.com/hynek/structlog) - Structured logging made easy.
- [loguru](https://github.com/Delgan/loguru) - Library which aims to bring enjoyable logging in Python.
- [logfire](https://github.com/pydantic/logfire) - The observability platform for Python, from the makers of Pydantic.

### Network Virtualization

_Tools and libraries for packet manipulation and network device automation._

- [scapy](https://github.com/secdev/scapy) - A brilliant packet manipulation library.
- [netmiko](https://github.com/ktbyers/netmiko) - Multi-vendor library to simplify CLI connections to network devices.
- [napalm](https://github.com/napalm-automation/napalm) - Cross-vendor API to manipulate network devices.

**CLI & GUI**

### CLI Development

_Libraries for building command-line applications._

- General
  - [argparse](https://docs.python.org/3/library/argparse.html) - (Python standard library) Command-line option and argument parsing.
  - [click](https://github.com/pallets/click) - A package for creating beautiful command line interfaces in a composable way.
  - [typer](https://github.com/fastapi/typer) - Modern CLI framework that uses Python type hints. Built on Click.
  - [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - A library for building powerful interactive command lines.
  - [cyclopts](https://github.com/BrianPugh/cyclopts) - Build CLIs from type-hinted functions, with docstring-based help.
- Terminal Rendering
  - [rich](https://github.com/Textualize/rich) - Python library for rich text and beautiful formatting in the terminal. Also provides a great `RichHandler` log handler.
  - [tqdm](https://github.com/tqdm/tqdm) - Fast, extensible progress bar for loops and CLI.
  - [colorama](https://github.com/tartley/colorama) - Cross-platform colored terminal text.
  - [alive-progress](https://github.com/rsalmei/alive-progress) - A new kind of Progress Bar, with real-time throughput, eta and very cool animations.
- TUI Frameworks
  - [textual](https://github.com/Textualize/textual) - A framework for building interactive user interfaces that run in the terminal and the browser.
  - [urwid](https://github.com/urwid/urwid) - A library for creating terminal GUI applications with strong support for widgets, events, rich colors, etc.
  - [asciimatics](https://github.com/peterbrittain/asciimatics) - A package to create full-screen text UIs (from interactive forms to ASCII animations).

### CLI Tools

_Useful CLI-based tools._

- Database CLIs
  - [pgcli](https://github.com/dbcli/pgcli) - PostgreSQL CLI with autocompletion and syntax highlighting.
  - [mycli](https://github.com/dbcli/mycli) - MySQL CLI with autocompletion and syntax highlighting.
  - [litecli](https://github.com/dbcli/litecli) - SQLite CLI with autocompletion and syntax highlighting.
  - [iredis](https://github.com/laixintao/iredis) - Redis CLI with autocompletion and syntax highlighting.
- Downloaders
  - [yt-dlp](https://github.com/yt-dlp/yt-dlp) - A command-line video downloader for YouTube and other sites, a fork of youtube-dl.
- HTTP Clients
  - [httpie](https://github.com/httpie/cli) - A command line HTTP client, a user-friendly cURL replacement.
- Project Scaffolding
  - [cookiecutter](https://github.com/cookiecutter/cookiecutter) - A command-line utility that creates projects from cookiecutters (project templates).
  - [copier](https://github.com/copier-org/copier) - A library and command-line utility for rendering project templates.
- Shells
  - [xonsh](https://github.com/xonsh/xonsh) - A Python-powered shell. Full-featured and cross-platform.
- Terminal Workflow
  - [tmuxp](https://github.com/tmux-python/tmuxp) - A [tmux](https://github.com/tmux/tmux) session manager.

### GUI Development

_Libraries for working with graphical user interface applications._

- Desktop
  - [PyGObject](https://github.com/GNOME/pygobject) - Python Bindings for GLib/GObject/GIO/GTK.
  - [dearpygui](https://github.com/hoffstadt/DearPyGui) - A simple GPU-accelerated Python GUI framework.
  - [Kivy](https://github.com/kivy/kivy) - An open-source cross-platform GUI framework for desktop, mobile, and embedded devices.
  - [wxPython](https://github.com/wxWidgets/Phoenix) - A cross-platform GUI toolkit that wraps the wxWidgets C++ library.
  - [toga](https://github.com/beeware/toga) - A Python native, OS native GUI toolkit.
- Qt
  - [PySide6](https://github.com/pyside/pyside-setup) - Qt for Python offers the official Python bindings for [Qt](https://www.qt.io/), largely API-compatible with PyQt6 but with different licensing.
  - [PyQt6](https://www.riverbankcomputing.com/static/Docs/PyQt6/) - Python bindings for the [Qt](https://www.qt.io/) cross-platform application and UI framework.
- Tkinter
  - [tkinter](https://docs.python.org/3/library/tkinter.html) - (Python standard library) The standard Python interface to the Tcl/Tk GUI toolkit.
  - [customtkinter](https://github.com/tomschimansky/customtkinter) - A modern and customizable Python UI-library based on Tkinter.
- Web-based
  - [pywebview](https://github.com/r0x0r/pywebview) - A lightweight cross-platform native wrapper around a webview component.
  - [nicegui](https://github.com/zauberzeug/nicegui) - An easy-to-use, Python-based UI framework, which shows up in your web browser.
  - [flet](https://github.com/flet-dev/flet) - Cross-platform GUI framework for building modern apps in pure Python.

**Text & Documents**

### Text Processing

_Libraries for parsing and manipulating plain texts._

- Encoding and Unicode
  - [charset-normalizer](https://github.com/jawah/charset_normalizer) - Universal character encoding detector, and a dependency of requests.
  - [chardet](https://github.com/chardet/chardet) - Python character encoding detector.
  - [ftfy](https://github.com/rspeer/python-ftfy) - Makes Unicode text less broken and more consistent automagically.
- Fuzzy Matching
  - [rapidfuzz](https://github.com/rapidfuzz/RapidFuzz) - Rapid fuzzy string matching using various string metrics, with a C++ core.
- General
  - [difflib](https://docs.python.org/3/library/difflib.html) - (Python standard library) Helpers for computing deltas.
  - [pyfiglet](https://github.com/pwaller/pyfiglet) - An implementation of figlet written in Python.
- Internationalization
  - [babel](https://github.com/python-babel/babel) - An internationalization library for Python.
- Parser
  - [pygments](https://github.com/pygments/pygments) - A generic syntax highlighter.
  - [pyparsing](https://github.com/pyparsing/pyparsing) - A Python library for creating PEG parsers.
  - [sqlparse](https://github.com/andialbrecht/sqlparse) - A non-validating SQL parser.
  - [phonenumbers](https://github.com/daviddrysdale/python-phonenumbers) - Parsing, formatting, storing and validating international phone numbers.
  - [parsy](https://github.com/python-parsy/parsy) - Easy, generic parser combinator library for creating parsers.
- Transliteration and Slugs
  - [python-slugify](https://github.com/un33k/python-slugify) - A Python slugify library that translates unicode to ASCII.
  - [unidecode](https://github.com/avian2/unidecode) - ASCII transliterations of Unicode text.
- Unique identifiers
  - [shortuuid](https://github.com/skorokithakis/shortuuid) - A generator library for concise, unambiguous and URL-safe UUIDs.

### HTML Manipulation

_Libraries for working with HTML and XML._

- [lxml](https://github.com/lxml/lxml) - A very fast, easy-to-use and versatile library for handling HTML and XML.
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Providing Pythonic idioms for iterating, searching, and modifying HTML or XML.
- [xmltodict](https://github.com/martinblech/xmltodict) - Working with XML feel like you are working with JSON.
- [markupsafe](https://github.com/pallets/markupsafe) - Safely adds untrusted strings to HTML/XML markup.
- [justhtml](https://github.com/EmilStenstrom/justhtml) - A pure Python HTML5 parser that sanitizes untrusted HTML by default.

### File Format Processing

_Libraries for parsing and manipulating specific file formats._

- General
  - [pyelftools](https://github.com/eliben/pyelftools) - Parsing and analyzing ELF files and DWARF debugging information.
  - [tablib](https://github.com/jazzband/tablib) - A module for Tabular Datasets in XLS, CSV, JSON, YAML.
- File Conversion
  - [markitdown](https://github.com/microsoft/markitdown) - Python tool for converting files and office documents to Markdown.
  - [pypandoc](https://github.com/JessicaTegner/pypandoc) - A thin wrapper for pandoc, the universal document converter.
  - [docling](https://github.com/docling-project/docling) - Library for converting documents into structured data.
- Excel
  - [openpyxl](https://openpyxl.readthedocs.io/en/stable/) - A library for reading and writing Excel 2010 xlsx/xlsm/xltx/xltm files.
  - [xlsxwriter](https://github.com/jmcnamara/XlsxWriter) - A Python module for creating Excel .xlsx files.
- Word
  - [python-docx](https://github.com/python-openxml/python-docx) - Creates, reads, and updates Microsoft Word (.docx) files.
- PowerPoint
  - [python-pptx](https://github.com/scanny/python-pptx) - Python library for creating and updating PowerPoint (.pptx) files.
- PDF
  - [pypdf](https://github.com/py-pdf/pypdf) - A library capable of splitting, merging, cropping, and transforming PDF pages.
  - [pymupdf](https://github.com/pymupdf/PyMuPDF) - A fast MuPDF-based library for extracting, rendering, and editing PDFs and other documents.
  - [reportlab](https://docs.reportlab.com/) - An open-source library for generating PDFs and graphics.
  - [pdfminer.six](https://github.com/pdfminer/pdfminer.six) - A community-maintained fork of PDFMiner for extracting information from PDF documents.
- HTML-to-PDF
  - [weasyprint](https://github.com/Kozea/WeasyPrint) - A visual rendering engine for HTML and CSS that can export to PDF.
- Markdown
  - [markdown-it-py](https://github.com/executablebooks/markdown-it-py) - Markdown parser with 100% CommonMark support, extensions, and syntax plugins.
  - [markdown](https://github.com/Python-Markdown/markdown) - A Python implementation of John Gruber’s Markdown.
  - [mistune](https://github.com/lepture/mistune) - A fast yet powerful Python Markdown parser with renderers and plugins.
- Data Formats
  - [tomllib](https://docs.python.org/3/library/tomllib.html) - (Python standard library) Parse TOML files.
  - [pyyaml](https://github.com/yaml/pyyaml) - A full-featured YAML framework for Python.

### File Manipulation

_Libraries for file manipulation._

- Paths and File Watching
  - [pathlib](https://docs.python.org/3/library/pathlib.html) - (Python standard library) A cross-platform, object-oriented path library.
  - [watchfiles](https://github.com/samuelcolvin/watchfiles) - Simple, modern and fast file watching and code reload in Python.
  - [watchdog](https://github.com/gorakhargosh/watchdog) - API and shell utilities to monitor file system events.
- File Type Detection
  - [mimetypes](https://docs.python.org/3/library/mimetypes.html) - (Python standard library) Map filenames to MIME types.
  - [python-magic](https://github.com/ahupp/python-magic) - A Python interface to the libmagic file type identification library.
  - [magika](https://github.com/google/magika) - Detects file content types with a deep-learning model.

**Media**

### Image Processing

_Libraries for manipulating images._

- Barcodes and QR Codes
  - [qrcode](https://github.com/lincolnloop/python-qrcode) - A pure Python QR Code generator.
  - [python-barcode](https://github.com/WhyNotHugo/python-barcode) - Create barcodes in Python with no extra dependencies.
- General
  - [pillow](https://github.com/python-pillow/Pillow) - Pillow is the friendly [PIL](https://pillow.readthedocs.io/en/stable/about.html) fork.
  - [scikit-image](https://github.com/scikit-image/scikit-image) - A Python library for (scientific) image processing.
  - [rembg](https://github.com/danielgatis/rembg) - A tool to remove image backgrounds.
  - [wand](https://github.com/emcconville/wand) - Python bindings for [MagickWand](https://imagemagick.org/magick-wand/), C API for ImageMagick.
  - [pyvips](https://github.com/libvips/pyvips) - A binding for libvips, a fast image processing library with low memory needs.
- Image Serving
  - [thumbor](https://github.com/thumbor/thumbor) - A smart imaging service. It enables on-demand crop, re-sizing and flipping of images.

### Audio & Video Processing

_Libraries for manipulating audio, video, and their metadata._

- Audio
  - [soundfile](https://github.com/bastibe/python-soundfile) - An audio library for reading and writing sound files, based on libsndfile, CFFI, and NumPy.
  - [librosa](https://github.com/librosa/librosa) - Python library for audio and music analysis.
  - [pydub](https://github.com/jiaaro/pydub) - Manipulate audio with a simple and easy high level interface.
- Video
  - [av](https://github.com/PyAV-Org/PyAV) - Pythonic bindings for FFmpeg's libraries.
  - [moviepy](https://github.com/Zulko/moviepy) - A module for script-based movie editing with many formats, including animated GIFs.
- Metadata
  - [mutagen](https://github.com/quodlibet/mutagen) - A Python module to handle audio metadata.
  - [tinytag](https://github.com/tinytag/tinytag) - A library for reading audio file metadata of MP3, MP4, WAV, OGG, FLAC, WMA, and AIFF files.
  - [beets](https://github.com/beetbox/beets) - A music library manager and [MusicBrainz](https://musicbrainz.org/) tagger.

### Game Development

_Awesome game development libraries._

- 3D Engines
  - [panda3d](https://github.com/panda3d/panda3d) - 3D game engine developed jointly by Disney and contributors from around the world.
- Game Frameworks
  - [pyglet](https://github.com/pyglet/pyglet) - A cross-platform windowing and multimedia library for Python.
  - [pygame-ce](https://github.com/pygame-community/pygame-ce) - An actively developed drop-in replacement with new features and performance improvements ([pygame](https://github.com/pygame/pygame) fork).
  - [pygame](https://github.com/pygame/pygame) - Pygame is a set of Python modules designed for writing games.
  - [arcade](https://github.com/pythonarcade/arcade) - An easy-to-use library for creating 2D arcade games.
- Visual Novels
  - [renpy](https://github.com/renpy/renpy) - A Visual Novel engine.

**Python Language**

### Implementations

_Implementations of Python._

- [cpython](https://github.com/python/cpython) - Default, most widely used implementation of the Python programming language written in C.
- [micropython](https://github.com/micropython/micropython) - A lean and efficient Python implementation for microcontrollers and constrained systems.
- [pypy](https://github.com/pypy/pypy) - A very fast and compliant implementation of the Python language.
- [Cython](https://github.com/cython/cython) - Optimizing Static Compiler for Python.
- [pyodide](https://github.com/pyodide/pyodide) - Python distribution for the browser and Node.js based on WebAssembly.

### Built-in Classes Enhancement

_Libraries for enhancing Python built-in classes._

- [attrs](https://github.com/python-attrs/attrs) - Replacement for `__init__`, `__eq__`, `__repr__`, etc. boilerplate in class definitions.
- [bidict](https://github.com/jab/bidict) - Efficient, Pythonic bidirectional map data structures and related functionality.
- [uuid-utils](https://github.com/aminalaee/uuid-utils) - A fast, Rust-backed drop-in replacement for Python's built-in `uuid` module.
- [python-box](https://github.com/cdgriffith/Box) - Python dictionaries with advanced dot notation access.

### Functional Programming

_Functional Programming with Python._

- [functools](https://docs.python.org/3/library/functools.html) - (Python standard library) Higher-order functions and operations on callable objects.
- [more-itertools](https://github.com/more-itertools/more-itertools) - More routines for operating on iterables, beyond `itertools`.
- [toolz](https://github.com/pytoolz/toolz) - A collection of functional utilities for iterators, functions, and dictionaries. Also available as [cytoolz](https://github.com/pytoolz/cytoolz) for Cython-accelerated performance.
- [funcy](https://github.com/Suor/funcy) - A fancy and practical functional tools.
- [returns](https://github.com/dry-python/returns) - A set of type-safe monads, transformers, and composition utilities.

### Asynchronous Programming

_Libraries for asynchronous, concurrent and parallel execution. Also see [awesome-asyncio](https://github.com/timofurrer/awesome-asyncio)._

- Async I/O
  - [asyncio](https://docs.python.org/3/library/asyncio.html) - (Python standard library) Asynchronous I/O, event loop, coroutines and tasks.
    - [awesome-asyncio](https://github.com/timofurrer/awesome-asyncio)
  - [anyio](https://github.com/agronholm/anyio) - A high-level async concurrency and networking framework that works on top of asyncio or trio.
  - [uvloop](https://github.com/MagicStack/uvloop) - Ultra fast asyncio event loop.
  - [trio](https://github.com/python-trio/trio) - A friendly library for async concurrency and I/O.
  - [gevent](https://github.com/gevent/gevent) - A coroutine-based Python networking library that uses [greenlet](https://github.com/python-greenlet/greenlet).
  - [Twisted](https://github.com/twisted/twisted) - An event-driven networking engine.
- Parallelism
  - [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) - (Python standard library) High-level asynchronous execution of callables.
  - [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) - (Python standard library) Process-based parallelism.

### Date and Time

_Libraries for working with dates and times._

- [zoneinfo](https://docs.python.org/3/library/zoneinfo.html) - (Python standard library) IANA time zone support. Brings the [tz database](https://en.wikipedia.org/wiki/Tz_database) into Python.
- [python-dateutil](https://github.com/dateutil/dateutil) - Extensions to the standard Python [datetime](https://docs.python.org/3/library/datetime.html) module.
- [dateparser](https://github.com/scrapinghub/dateparser) - A Python parser for human-readable dates in over 200 language locales.
- [pendulum](https://github.com/python-pendulum/pendulum) - Python datetimes made easy.
- [whenever](https://github.com/ariebovenberg/whenever) - A modern datetime library, type-safe and DST-safe, in Rust or pure Python.

**Python Toolchain**

### Environment Management

_Libraries for Python version and virtual environment management._

- [virtualenv](https://github.com/pypa/virtualenv) - A tool to create isolated Python environments.
- [uv](https://github.com/astral-sh/uv) - An extremely fast Python version, package and project manager, written in Rust.
- [pyenv](https://github.com/pyenv/pyenv) - Simple Python version management.
- [mise](https://github.com/jdx/mise) - A polyglot tool version manager that installs Python versions and reads .python-version files.

### Package Management

_Libraries for package and dependency management._

- Package Managers
  - [pip](https://github.com/pypa/pip) - The package installer for Python.
  - [uv](https://github.com/astral-sh/uv) - An extremely fast Python version, package and project manager, written in Rust.
  - [poetry](https://github.com/python-poetry/poetry) - Python dependency management and packaging made easy.
  - [hatch](https://github.com/pypa/hatch) - Modern, extensible Python project manager for environments, builds, and publishing.
  - [pipx](https://github.com/pypa/pipx) - Install and Run Python Applications in Isolated Environments. Like `npx` in Node.js.
  - [conda](https://github.com/conda/conda) - Cross-platform, Python-agnostic binary package manager.
- Build Backends
  - [setuptools](https://github.com/pypa/setuptools) - The historical and still most widely used pyproject build backend.
  - [hatchling](https://github.com/pypa/hatch) - Modern, extensible build backend from the hatch project.
  - [poetry-core](https://github.com/python-poetry/poetry-core) - Poetry's PEP 517 build backend, usable without Poetry itself.
  - [flit-core](https://github.com/pypa/flit) - Minimal, dependency-free build backend for pure-Python packages.
  - [uv-build](https://github.com/astral-sh/uv) - uv's fast, minimal build backend for pure-Python projects.

### Package Repositories

_Local PyPI repository servers, proxies, and mirrors._

- [pypiserver](https://github.com/pypiserver/pypiserver) - A minimal PyPI server for uploading and installing packages with pip.
- [devpi](https://github.com/devpi/devpi) - PyPI server and packaging/testing/release tool.
- [bandersnatch](https://github.com/pypa/bandersnatch) - PyPI mirroring tool provided by Python Packaging Authority (PyPA).

### Distribution

_Libraries to create packaged executables for release distribution._

- Executables
  - [pyinstaller](https://github.com/pyinstaller/pyinstaller) - Converts Python programs into stand-alone executables (cross-platform).
  - [Nuitka](https://github.com/Nuitka/Nuitka) - Compiles Python programs into high-performance standalone executables (cross-platform).
  - [pex](https://github.com/pex-tool/pex) - A tool for building self-contained Python executable environments (PEP 441 zipapps).
  - [cx-Freeze](https://github.com/marcelotduarte/cx_Freeze) - Converts Python scripts into standalone executables and installers for Windows, macOS, and Linux.
- Obfuscation
  - [pyarmor](https://github.com/dashingsoft/pyarmor) - A tool used to obfuscate Python scripts, bind obfuscated scripts to fixed machine or expire obfuscated scripts.

### Configuration Files

_Libraries for storing and parsing configuration options._

- [configparser](https://docs.python.org/3/library/configparser.html) - (Python standard library) INI file parser.
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Reads key-value pairs from a `.env` file and sets them as environment variables.
- [pydantic-settings](https://github.com/pydantic/pydantic-settings) - Settings management using Pydantic models with validation, loading from environment variables and secrets files.
- [hydra-core](https://github.com/hydra-ecosystem/hydra) - Hydra is a framework for elegantly configuring complex applications.
- [dynaconf](https://github.com/dynaconf/dynaconf) - Dynaconf is a configuration manager with plugins for Django and Flask.

**Security**

### Cryptography

_Libraries for cryptographic primitives and secure protocols._

- [cryptography](https://github.com/pyca/cryptography) - A package designed to expose cryptographic primitives and recipes to Python developers.
- [pynacl](https://github.com/pyca/pynacl) - Python binding to libsodium, a fork of the Networking and Cryptography (NaCl) library.
- [paramiko](https://github.com/paramiko/paramiko) - The leading native Python SSHv2 protocol library.
- [itsdangerous](https://github.com/pallets/itsdangerous) - Safely pass trusted data to untrusted environments and back.

### Penetration Testing

_Frameworks and tools for penetration testing._

- [mitmproxy](https://github.com/mitmproxy/mitmproxy) - An interactive TLS-capable intercepting HTTP proxy for penetration testers and software developers.
- [impacket](https://github.com/fortra/impacket) - A collection of Python classes for working with network protocols, widely used for Windows and Active Directory testing.
- [sqlmap](https://github.com/sqlmapproject/sqlmap) - Automatic SQL injection and database takeover tool.
- [pwntools](https://github.com/Gallopsled/pwntools) - A CTF framework and exploit development library.
- [sherlock-project](https://github.com/sherlock-project/sherlock) - Hunt down social media accounts by username across social networks.

### Supply Chain Security

_Tools for auditing dependencies against known vulnerabilities and scanning for leaked secrets._

- Dependency Audits
  - [pip-audit](https://github.com/pypa/pip-audit) - Audits Python environments and dependency trees for known vulnerabilities, using the Python Packaging Advisory Database or OSV.
  - [uv-audit](https://github.com/astral-sh/uv) - (part of uv) uv's [dependency vulnerability scanning](https://docs.astral.sh/uv/reference/cli/#uv-audit) backed by OSV.
- Secret Scanning
  - [betterleaks](https://github.com/betterleaks/betterleaks) - Finds leaked secrets in git history, directories, and files, from the original author of gitleaks.

### Web Security

_Libraries for application-layer web security._

- [nh3](https://github.com/messense/nh3) - Python binding to the ammonia HTML sanitizer, a fast replacement for bleach.
- [secure](https://github.com/TypeError/secure) - HTTP security headers for Python web applications with ASGI and WSGI middleware.

**Other**

### Hardware

_Libraries for programming with hardware._

- [pyserial](https://github.com/pyserial/pyserial) - Python serial port access library for Windows, macOS, Linux, and BSD.
- [pynput](https://github.com/moses-palmer/pynput) - A library to control and monitor input devices.
- [bleak](https://github.com/hbldh/bleak) - A cross platform Bluetooth Low Energy Client for Python using asyncio.
- [jumpstarter](https://github.com/jumpstarter-dev/jumpstarter) - A hardware-in-the-loop testing framework with a Python client library for automated testing on real and virtual hardware.

### Microsoft Windows

_Python programming on Microsoft Windows._

- [pywin32](https://github.com/mhammond/pywin32) - Python Extensions for Windows.
- [pythonnet](https://github.com/pythonnet/pythonnet) - Python Integration with the .NET Common Language Runtime (CLR).
- [pyenv-win](https://github.com/pyenv-win/pyenv-win) - A Python version manager for Windows ([rbenv-win](https://github.com/nak1114/rbenv-win) fork).
- [winpython](https://github.com/winpython/winpython) - Portable Python distribution for Windows.

### Miscellaneous

_Useful libraries or tools that don't fit in the categories above._

- [blinker](https://github.com/pallets-eco/blinker) - A fast Python in-process signal/event dispatching system.
- [boltons](https://github.com/mahmoud/boltons) - A set of pure-Python utilities.

## Resources

Where to discover learning resources or new Python libraries.

### Newsletters

- [Awesome Python Newsletter](https://python.libhunt.com/newsletter)
- [Pycoder's Weekly](https://pycoders.com/)
- [Python Tricks](https://realpython.com/python-tricks/)
- [Python Weekly](https://www.pythonweekly.com/)

### Podcasts

- [Django Chat](https://djangochat.com/)
- [PyPodcats](https://pypodcats.live)
- [Python Bytes](https://pythonbytes.fm)
- [Talk Python To Me](https://talkpython.fm/)
- [The Real Python Podcast](https://realpython.com/podcasts/rpp/)

### Websites

- [Python Developer Tooling Handbook](https://pydevtools.com/) - Comprehensive guide to modern Python developer tools covering package management, linting, type checking, testing, and more.

## Contributing

Your contributions are always welcome! Please take a look at the [contribution guidelines](https://github.com/vinta/awesome-python/blob/master/CONTRIBUTING.md) first.

---

If you have any question about this opinionated list, do not hesitate to contact [@vinta](https://x.com/vinta) on X (Twitter).



================================================
FILE: AGENTS.md
================================================
# AGENTS.md

An opinionated guide to the best Python frameworks, libraries, and tools.

[README.md](README.md) is the source of truth for entries, and `website/data/category_intros/` holds the category page intros; `website/` renders both into [awesome-python.com](https://awesome-python.com/).

## Entry Rules

Apply [CONTRIBUTING.md](CONTRIBUTING.md) (admission, entry format, ordering) whenever adding, removing, or rewording an entry, direct commits included.

- Verify every keep/drop reason against current online data at decision time: download counts, repo activity and archived status, PyPI metadata, project docs. Tier calls (obvious choice vs challenger) also need WebSearch evidence of adoption trajectory and community sentiment. Training-data recollections are not evidence; label anything unverifiable as a judgment call.
- Checks stay read-only: judge whether a listed project installs or works from its PyPI metadata (`requires_python`, classifiers, wheel tags) and issue tracker, never by installing or running it, since that runs untrusted code.
- A download count is not automatically independent demand. When one listed entry depends on another, check `requires_dist` on PyPI before citing the depended-on entry's count: mkdocs-material hard-depends on mkdocs, so mkdocs' figure exceeded mkdocs-material's by only about one percent and nearly all of it was mkdocs-material pulling it in.
- One entry per commit when adding or deleting entries. Exceptions: a prune sweep is one commit per section, its body listing each removal with its reason; format, wording, or categorization changes may be bundled. Cross-section re-homes ride the originating audit's commit (both sides of the move in one diff).
- Resources sections are not project entries: out of audit scope, and the website never parses them.
- Sponsor placement never influences which projects get listed — see [SPONSORSHIP.md](SPONSORSHIP.md).

## Website

Read [DESIGN.md](DESIGN.md) before changing anything under `website/templates/` or `website/static/`.



================================================
FILE: CLAUDE.md
================================================
@AGENTS.md



================================================
FILE: CODE_OF_CONDUCT.md
================================================
# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone, regardless of age, body
size, visible or invisible disability, ethnicity, sex characteristics, gender
identity and expression, level of experience, education, socio-economic status,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

## Our Standards

Examples of behavior that contributes to a positive environment:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior:

- The use of sexualized language or imagery
- Trolling, insulting or derogatory comments
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the project maintainers. All complaints will be reviewed and
investigated and will result in a response that is deemed necessary and
appropriate to the circumstances.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant](https://www.contributor-covenant.org),
version 2.0.



================================================
FILE: CONTRIBUTING.md
================================================
# Contributing

awesome-python is a shortlist, not a catalog. Each use case lists only its obvious choices, and most rejections mean "the use case is full", not "your project is bad". Read this whole page before opening a PR.

## Quality Requirements

All submissions must satisfy **ALL** of these:

1. **Serves Python Developers**: Python developers use it in their Python work. Implementation language and packaging are irrelevant — uv and ty are written in Rust, and agent skill packs are markdown, yet all belong; a pure-Python project nobody uses in Python work does not.
2. **Active**: Commits within the last 12 months
3. **Stable**: Production-ready, not alpha/beta/experimental. A PyPI "Development Status" classifier alone does not decide this; judge by releases, documentation, and production use.
4. **Documented**: Clear README with examples and use cases
5. **Established**: Repository at least 1 month old

## Admission

A **use case** is one distinct job a reader needs done. Use cases are defined by the list's structure: each subcategory is a use case, and a section without subcategories is a single use case. Structure changes — new sections, new subcategories, splitting an oversized use case into finer ones — are made only by the maintainer; an entry PR can never create the subcategory it needs.

Each use case lists at most:

- **Up to 3 obvious choices** — tools an experienced Python developer would name when asked "what do I use for this?"
- **Up to 2 challengers** — tools that are not yet the obvious choice but are credible successors to one. Admission as a challenger requires adoption-trajectory evidence, not popularity alone.

Hard maximum: 5 entries per use case. This is a qualitative bar first and a numeric backstop second — most use cases should carry fewer.

**Overrides**: the maintainer may exceed any limit on this page — the caps, the activity requirement, the stability requirement — for a specific entry or use case by explicit decision. An override is case-by-case; it does not loosen these rules for submissions, and citing one in a PR carries no weight.

**Displacement**: once a use case is at its cap, the only way in is to name the entry your project replaces and argue that yours does that entry's job better. One in, one out.

**Dual-listing**: a tool may hold entries in multiple use cases, but only when it is an obvious choice in each. List the full entry in each home with identical lines; never a "see X above" note, since the website only renders list items. Description edits update every copy in the same commit. Each slot is audited on its own: dropping one home keeps the other, and dropping the tool entirely removes all copies in one commit. Dual-listing is a maintainer decision; a PR adding a second home for an existing entry is treated as a duplicate.

**Standard library**: a standard-library module is listed only where the stdlib is itself the obvious choice for the use case (tomllib yes, unittest no).

**Python versions**: missing support for the newest Python releases is not by itself grounds for removal while the entry still has a large user base; it can place the entry in the Second Tier instead.

**Second Tier**: a challenger slot held by a demoted former obvious choice instead of a rising successor. It counts against the two challenger slots, and the adoption-trajectory bar gates only new admissions, not demotions.

**Evidence**: admission is decided by maintainer editorial judgment, informed primarily by PyPI download counts rather than GitHub stars. Judgment overrides the signal's known failure modes (CI-inflated counts, model releases consumed as weights rather than pip installs, projects used outside pip such as SDK downloads (renpy) or deployed services (thumbor), large-but-specific audiences misread as "niche"). The maintainer's decision is final.

Looking for an exhaustive catalog instead? Follow the awesome-\* lists linked under individual entries (for example awesome-python-testing) — they exist precisely so this list doesn't have to be one.

## Entry Format Reference

**Use GitHub repository URLs** whenever possible. [awesome-python.com](https://awesome-python.com/) shows stars and last-commit dates only for GitHub repos, and ranks entries without PyPI downloads by stars.

### Naming Convention

Use the **PyPI package name** as the display name so developers can copy it directly to `pip install`. Check the canonical name at `https://pypi.org/pypi/{package}/json`. If the project is not on PyPI, use the GitHub repository name instead.

### Standard Entry

```markdown
- [pypi-name](https://github.com/owner/repo) - Description ending with period.
```

### Description Length

Aim for a rendered line of 100 characters or fewer: the name, ` - `, and the description, not counting the URL. Lines that long fit on one line in the GitHub README, which starts wrapping them around 105. This is a soft cap. When a draft lands near 105, cut filler words to get under it; when the content needs more room, let the line wrap rather than drop meaning.

### Standard Library Module

```markdown
- [module](https://docs.python.org/3/library/module.html) - (Python standard library) Description.
```

### Bundled Feature

A feature that ships inside a larger library, framework, or tool rather than as its own PyPI package. The `(part of X)` prefix is parsed by the website, which renders a "Bundled" badge in place of a download count, so write it exactly in that form and name the parent as developers say it.

```markdown
- [name](url) - (part of Parent) Description ending with period.
```

### Fork of Another Project

```markdown
- [new-name](https://github.com/owner/new-name) - Description ([original-name](original-url) fork).
```

### Entry with Related Awesome List

```markdown
- [project](https://github.com/owner/project) - Description.
  - [awesome-project](https://github.com/someone/awesome-project)
```

Only awesome-\* lists go here, placed by the maintainer. A sub-item holds no slot, does not count against the cap, and moves or goes away with its parent. A companion project either earns its own entry or is not listed.

### Subcategory Format

```markdown
- Subcategory Name
  - [project](url) - Description.
```

### Entry Ordering

Within a use case, the obvious choices are listed first, ordered by PyPI downloads per month from high to low; challengers follow, in the same order. Standard-library modules sort first in the use case — built-ins lead, before everything else — alphabetically when there are several. (This never conflicts with tier order: a standard-library module is only listed where it is itself the obvious choice, so it always belongs to the first tier.) Other entries without a download signal (agent skill packs, projects distributed outside PyPI) sort last within their tier, alphabetically. There is no marker in the entry text — position is the marker, so the last entries of a use case may be its challengers.

## Changing the Structure

Adding sections or subcategories is maintainer-only (see Admission). For maintainer reference:

1. Add the section description in italics: `*Libraries for doing X.*`
2. Add the section under the appropriate thematic group (e.g., **AI & ML**, **Web**, **Data & Science**)
3. Add the section title to the Table of Contents under its group
4. Order entries per Entry Ordering above

A subcategory never repeats its section's name: one named like its section competes with the section page in search results. Name the section's catch-all or main use case General instead.

## Review Process

PRs are reviewed by automated tools and maintainers:

1. **Format Check**: Entry follows the correct format
2. **Category Check**: Placed in the appropriate use case
3. **Duplicate Check**: Not already listed or previously rejected
4. **Activity Check**: Project shows recent activity
5. **Admission Check**: Meets the Admission rules above, including Displacement when the use case is at its cap

Search previous Pull Requests and Issues before submitting, as yours may be a duplicate.

## Automatic Rejection

PRs will be **closed** if:

- Adding multiple projects in one PR
- The use case is at its cap and the PR makes no Displacement argument
- The PR creates a new section or subcategory and fills it (structure changes are maintainer-only)
- Coordinated multi-entry self-promotion: multiple related projects from the same organization or author, across one or several PRs
- Duplicate of existing entry or recently-closed PR
- Empty or placeholder PR descriptions
- Placed under an inappropriate category
- Project is archived or abandoned (no commits in 12+ months)
- No documentation or unclear use case
- Repository less than 1 month old



================================================
FILE: DESIGN.md
================================================
---
version: alpha
name: awesome-python.com
description: Warm editorial Python index. Light cream canvas, brown-red interactive accent, Cormorant Garamond plus Manrope, table-driven reference.
---

# awesome-python.com DESIGN.md

awesome-python.com is a searchable, filterable index of curated Python projects. It is a reference tool, not a landing page and not a GitHub README mirror.

This file follows the [Google Stitch DESIGN.md format](https://stitch.withgoogle.com/docs/design-md/overview). Token values live in `website/static/style.css`; this file names each token's role. Colors are OKLCH, a deliberate divergence from the spec's hex-only token requirement.

## Overview

Three words: **opinionated, confident, dense**.

Working Python developers (mid to senior) are the target reader. They write Python daily and arrive with a specific question in mind: "what's a good HTTP client these days", "is there still a maintained ORM for X", "what are people using for task queues now". Secondary readers: polyglot developers evaluating Python's ecosystem, and curious browsers.

Jobs to be done:

1. Find a library for a specific need fast (search + tag filter).
2. Compare candidates at a glance (downloads, stars, last commit, tags, one-line description).
3. Confirm a project is alive before clicking through.

These users skim. They reward density and terse copy. They penalize marketing fluff.

Voice:

- Editorial. Every word earns its place.
- Confident, not combative. "This is the list" energy, not "check out these cool projects".
- No hype. The content is what's interesting.
- Calm authority. Closer to a well-edited technical reference (O'Reilly index, The Economist briefing, a good man page) than a blog or product site.

Emotional goals: trust, efficiency, craft. The reader should feel the list was edited by someone with taste, find what they need in seconds, and notice the typographic care as a signal that the curation is careful too.

Reference points (stay close to these):

- **https://www.placestoread.xyz** is the primary visual model for the table, expand row, sorting, and footer. "Like placestoread" means a dense list (the home page holds every project in one table), inline click-to-expand rows that indent under the Name column, sortable headers, a divider under the header row instead of a strong top border, minimum decoration. When in doubt about a table or row treatment, check placestoread first.
- Magazine reference pages (The Economist, FT Weekend, Monocle).
- Field-guide books. Curated, functional, hand-made.
- Library card catalogs. Dense tabular information, excellent typography, no decoration for decoration's sake.

Anti-references (avoid strictly):

- Generic dark developer-tool look. No cyan on near-black, neon gradients, VSCode-palette dashboards, terminal-green monospace branding.
- Other awesome-\* sites. No plain README dumps, bare lists of links, no voice.
- SaaS marketing pages. No big metric counters, testimonial cards, feature grids, pricing tiers, or "join 10,000+ developers" social proof bands.

Design principles:

1. **The list is the hero.** Hero, sponsor band, and CTA exist, but they must not compete with the table for attention.
2. **Density is a feature.** Prefer tables and tight rhythm over giant cards with one fact each. Mid-senior developers want to see more at once.
3. **Editorial typography over decoration.** Visual interest comes from the serif/sans pairing, type hierarchy, and whitespace. Not from gradients, shadows, badges, or icon boxes above headings.
4. **Warm, not cool.** Neutrals tint toward warm hues (roughly 55 to 80 in OKLCH). Pure grays and cool blues do not belong.
5. **One point of view.** No dark mode, no theme picker, no alternate palettes. Consistency signals curation.

## Colors

Warm editorial palette. Light theme only (`color-scheme: light`). OKLCH only.

Surfaces:

- `--bg-page`. Cream/ivory canvas, the body floor. The body uses a vertical gradient from `--bg-page-top` through `--bg-page` (at 24rem) to `--bg-page-end`, with a soft radial highlight in the top-left corner.
- `--bg-paper`. Warm white for the content shell.
- `--bg-paper-strong`. Tinted paper for CTA backgrounds and static decoration.
- `--sponsor-bg`. Deeper warm tint for the sponsor band only, so it reads as its own block between the hero and the table.
- `--hero-bg-start` → `--hero-bg-mid` → `--hero-bg-end`. Dark earthy hero gradient.
- `--footer-bg`. Dark warm charcoal footer, part of the same system.

Ink:

- `--ink`. Body text.
- `--ink-soft`. Secondary copy.
- `--ink-muted`. Meta rows, captions, static labels.
- `--line` / `--line-strong`. Hairlines and dividers.

Accent (warm brown-red, reserved for interactive):

- `--accent`. Primary accent.
- `--accent-deep`. Link text, hover.
- `--accent-soft`. Tinted background for filter tags.
- `--accent-underline`. Subtle text-decoration-color.

Rules:

- Use OKLCH for any new color. Not HSL, not hex.
- Accent tokens (`--accent`, `--accent-deep`, `--accent-soft`) are reserved for interactive elements. Clickable filter tags (`.tag`) correctly use `--accent-soft` background with `--accent-deep` text. Interactive link states (`.col-name > a:hover`, `.sponsor-link:hover`, `.hero-action-primary`, `.back-to-top`, CTAs) use accent tokens.
- Non-interactive elements (inline code, `.source-badge`, static labels, decorative pills) must use ink tokens (`--ink`, `--ink-soft`, `--ink-muted`) on `--bg-paper-strong` or `--bg-paper`, never the accent. `.source-badge` uses `--ink-soft`; `.sponsorship-body code` uses `--ink`. Users should not mistake static decoration for something clickable.
- Same role uses the same token everywhere. No one-off inline `color: oklch(...)` buried in a rule.

Aversions:

- **No green.** The maintainer rejected it when picking the palette. Warm brown-red, ivory, and dark earthy tones are the established system. Do not introduce green even for success states or ancillary accents.
- No cyan, no neon gradients, no pure grays, no cool blues.

## Typography

Pairing (do not swap):

- **Display**: `Cormorant Garamond` (serif, 600 only).
- **Body**: `Manrope` (sans, 400 / 600 / 700 / 800).

Cormorant Garamond sets headings and standalone names only, never running sentences, and never on the same line as Manrope. Its short x-height and thin strokes tire the eye across a paragraph, and next to Manrope on one baseline the two x-heights clash. Ledes and other multi-line copy use Manrope (`--text-2xl`); a display name with a description stacks the name above it, as in the sponsor band.

Scale:

| Role             | Token             | Size                             | Family             | Weight    | Notes                                             |
| ---------------- | ----------------- | -------------------------------- | ------------------ | --------- | ------------------------------------------------- |
| Hero headline    | (literal `clamp`) | `clamp(4.5rem, 11vw, 8.5rem)`    | Cormorant Garamond | 600       | Magazine-cover scale, single use on the hero      |
| Page title       | `--display-lg`    | `clamp(3.6rem, 9vw, 7rem)`       | Cormorant Garamond | 600       | Category and sponsorship `h1`                     |
| Section heading  | `--display-md`    | `clamp(2.25rem, 4.2vw, 3.3rem)`  | Cormorant Garamond | 600       | Guide, results, CTA `h2`, sponsor name            |
| Display small    | `--display-sm`    | `clamp(1.75rem, 2.8vw, 2.25rem)` | Cormorant Garamond | 600       | Group-row `h2`, past sponsor names                |
| Lede             | `--text-2xl`      | `1.5rem`                         | Manrope            | 400       | Category intro first paragraph, sponsorship ledes |
| Subtitle         | `--text-xl`       | `1.25rem`                        | Manrope            | 400       | Hero and category subtitles, category intro       |
| Body large       | `--text-lg`       | `1.125rem`                       | Manrope            | 400       | Content-heavy passages, project names, search     |
| Body             | `--text-base`     | `1rem` (16px)                    | Manrope            | 400       | Body floor                                        |
| Meta / secondary | `--text-sm`       | `0.95rem`                        | Manrope            | 400 / 600 | Meta rows, secondary copy                         |
| Caption / pill   | `--text-xs`       | `0.8rem` (12.8px)                | Manrope            | 600 / 700 | Smallest token, pills, badges, tags, footnotes    |

Hard-won sizing rules (do not relax):

- **Every `font-size` uses a scale token.** The literal exceptions are the hero headline, `.tier-amount`, the sort `.arrow` glyph, and `em` sizes on inline code and `kbd`. Body tokens are fixed `rem`; only display tokens are fluid, because `vw` in body text does not grow with browser zoom. Round a new size up to the next token instead of adding an in-between step: sizes 1 to 2px apart read as noise, not hierarchy.
- **Body type floor is 16px.** Do not go smaller.
- **Absolute minimum font size is 12px (`0.75rem`) for ANY text**, including pills, badges, tags, captions, footnotes. Anything smaller hits Chrome's default minimum-font-size floor and renders inconsistently across browsers and user accessibility settings.
- **When in doubt, pick one step larger** than what generic scale references suggest (`--text-base` over `--text-sm`, 1.75rem over 1.5rem for a heading). The maintainer has corrected sizes upward 11+ times across 8 sessions. Footer, meta rows, expand content, labels, and headings all trend too small by default. **Never reduce an existing size unprompted.**
- Adjacent heading levels differ by at least 0.25rem of rendered size.
- Row numbers in the table: left-align, no leading zeros. Zero-padding was tried and rejected.
- **Cormorant Garamond numerals use lining figures** (`font-variant-numeric: lining-nums`). Its default old-style figures shrink zeros to x-height and drop 3/4/5/7/9 below the baseline, so a price like `$500` reads as `$5oo`.
- **Never `text-transform`.** Write the casing in the markup.

## Layout

- **Single width cap: `--shell-max: 84rem` (~1344px) applied via `.section-shell`.** This is the ONLY width cap in the project. Widescreen monitors are the default viewing context.
- **Do NOT add `max-width`** to sections, cards, table cells, table rows, expanded rows, CTA backgrounds, sponsor descriptions, hero subcopy, paragraphs, or list items. The maintainer has removed narrow inner caps repeatedly (`56ch`, `65-75ch`, etc.). Default is no inner cap; remove any inner cap you come across. The "cap line length at ~65-75ch" rule does NOT apply here: readability at wide widths is carried by vertical rhythm, leading, and the modular type scale instead.
- If a width cap is genuinely necessary for a specific element, ask first with a concrete reason before adding it.
- Shell padding: `--shell-pad: clamp(1.25rem, 3vw, 2.5rem)`. Symmetric gutters: logo left-gap equals logo right-gap, column paddings match across header and body.
- `gap` over child margins in flex and grid.
- Logical properties (`margin-inline`, `padding-block`) over physical (`margin-left`, `padding-top`).
- `rem` for spacing and type. `px` only for borders and shadows.
- CSS custom properties for all colors and repeated values.
- Sibling components (card lists, grid items) share identical spacing.
- Use flexbox or grid for layout. Avoid floats and absolute positioning except for genuine overlay cases (focus rings, sticky headers).
- Never `!important`, except in the `prefers-reduced-motion` reset. Fix specificity instead.

## Elevation & Depth

Depth comes from **tonal layers**, not heavy shadows.

- The page is a quiet warm canvas (`--bg-page`). The content shell is slightly brighter paper (`--bg-paper`). CTA backgrounds and inline decorative blocks step up to `--bg-paper-strong`; the sponsor band steps further, to `--sponsor-bg`.
- The hero and the category guide band are the only places with real atmosphere: warm gradients on a dark earthy ground (`--hero-bg-start` → `--hero-bg-mid` → `--hero-bg-end`). Only the hero adds the subtle grid. The hero background holds still: a moving stripe on a narrow phone hero reads as a loading bar. Any motion elsewhere respects `prefers-reduced-motion`.
- The footer is a single tonal block in `--footer-bg`, no internal gradients.
- Two depth treatments are allowed and only these two. The search input combines a 1px inset highlight (`--search-inset`) with a soft warm drop shadow (`--search-shadow`, intensified by `--search-focus-shadow` on focus). The primary CTA button (`.hero-action-primary`) carries a warm drop shadow for press affordance. Both shadows are soft, warm-tinted, and tied to interactive elements. No new drop shadows on cards, panels, rows, or static decoration.
- No glassmorphism as default decoration.
- No bounce or elastic easing. Real objects decelerate smoothly.

## Shapes

The shape language is overwhelmingly **pill on small, zero radius on large**.

- **Pills** (`border-radius: 999px`) for tags, search, sponsor logo chip, source badges, back-to-top, and primary CTA buttons.
- **`0.4rem`** is used only on inline `<code>` in category intros, the guide band, and `.sponsorship-body`. Do not introduce a tokenized radius scale. The project does not need one.
- Containers use the page surface itself, not rounded panels. When a panel is needed, prefer pill on small chips and zero radius on large surfaces.
- **No `border-left` or `border-right` greater than 1px as a colored accent stripe** on cards, list items, callouts, or alerts. Use a different structure.

## Components

The component vocabulary is small and table-led. Source of truth: `website/static/style.css`.

- **Table-driven index** (the hero of the page). Sticky header, sortable columns, click-to-expand rows that indent under the Name column. Modeled on placestoread.xyz. Not a card grid.
- **Group rows**. Section, subcategory, and group pages list rows in README order. Section pages add one H2 row per use case; group pages add one per section, linking to that section's page. A note replaces the sort arrow until someone sorts a column, which flattens the list and hides the group rows.
- **Filter tags** (`.tag`). `--accent-soft` background with `--accent-deep` text. Pill shape. Hover swaps to `--highlight` background with `--tag-hover-border` border and ink text. Active state uses the warm `--tag-active-start` → `--tag-active-end` gradient with hero-ink text. Tag variants (`tag-group`, `tag-source`) inherit the base `.tag` style today and differ only at narrow widths (`tag-group` hides under 960px). Add a new variant only when a real visual difference is needed.
- **Hero**. Magazine-cover headline, dark earthy ground, kicker and proof microcopy, primary CTA button using `--hero-btn-start` / `--hero-btn-end`. Subtle grid on a still background.
- **Jump links**. One per use case in a category hero, plus one for the guide. Underlined like the intro's links, with a trailing ↓. Never tag-styled: tags filter the table or open another page, jump links only scroll.
- **Guide band**. Everything in a category intro after its "How to choose" list. It sits below the table on the hero's dark gradient, with its H2 above the text.
- **Sponsor band**. Sits below the hero on the home page and category pages, on `--sponsor-bg` with a `--line-strong` bottom border. Editorial layout, not a logo wall. Sponsor links share the global accent treatment; each sponsor name ends in a small ↗ in `--accent-deep` to mark it as an outbound link.
- **CTA**. Warm `--cta-bg`, full-bleed within shell. The button itself uses accent tokens.
- **Footer**. Dark warm charcoal, part of the same system. Footer links share the global hover and focus treatment.
- **Search**. Pill input with `--search-inset` interior and `--search-focus-ring` focus ring. Focus shadow uses `--search-focus-shadow`.
- **Source badge / inline code**. Static decoration on `--bg-paper-strong`. `.source-badge` uses `--ink-soft` text in pill shape; `.sponsorship-body code` uses `--ink` text with the `0.4rem` radius. Never the accent.

## Do's and Don'ts

- **Don't** replace the table with a card grid, modal details, or pagination.
- **Don't** use gradient text (`background-clip: text` on gradients). Solid color only.

## Narrow-Screen Behavior

The maintainer actively tests `< 960px` and `< 680px`. Narrow screens must stay functional.

- Do not drop features readers might want (sort affordance, filter chips, sticky header where reasonable). Hiding is a last resort and requires justification.

## Iteration Guide

Run this audit after generating or modifying a screen. Failure on any item means revise before moving on.

1. **Width caps.** Inspect every section, card, paragraph, table cell, expanded row, CTA, sponsor description, hero subcopy. Only `.section-shell` (`--shell-max: 84rem`) may cap width. Anything else with a `max-width` is wrong.
2. **Accent reservation.** Grep the changed CSS for `--accent`, `--accent-deep`, `--accent-soft`. Each match must back an interactive element (link, button, focus ring, filter tag). Static decoration must use ink tokens (`--ink`, `--ink-soft`, `--ink-muted`) on `--bg-paper-strong` or `--bg-paper`.
3. **Shape language.** Containers are square or pill. Anything in the 4px-to-16px radius range is suspect. The `0.4rem` on inline code is the only allowed exception.
4. **Type sizes.** Confirm no rendered text falls below 12px. If a size feels small to a mid-senior reader on a 27-inch display, bump one step up. Never reduce an existing size.
5. **Peer consistency.** Compare against the closest peer element. Peer links (hero topbar, footer, project names, sponsor names, expand-meta) share hover and focus treatment; tag variants inherit the base `.tag` style; labels that play the same role share size, weight, and letter-spacing. Color token and gutter must match unless there is a stated reason to differ.
6. **Browser check.** Run the `playwright-cli` skill at full width, `< 960px`, and `< 680px`. Check layout and interactive behavior; sort affordance, filter chips, and sticky header must remain functional. Do not claim a UI change works based on code alone.

## Known Gaps

- **No formal spacing or radius scale.** The codebase uses `clamp()` and ad-hoc rem values rather than a tokenized scale. Adding one would be invention, not documentation.



================================================
FILE: LICENSE
================================================
Creative Commons Attribution 4.0 International License (CC BY 4.0)

http://creativecommons.org/licenses/by/4.0/



================================================
FILE: Makefile
================================================
-include .env
export

install:
	uv sync --locked

fetch_github_stars:
	uv run python website/fetch_github_stars.py

fetch_pypi_downloads:
	uv run python website/fetch_pypi_downloads_via_clickpy.py

test:
	uv run pytest website/tests/ -v

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run ty check website

build:
	uv run python website/build.py

preview: build
	uv run watchfiles \
		'uv run python website/build.py' \
		README.md website/templates website/static website/data & \
	python -m http.server -b 127.0.0.1 -d website/output/ 8000



================================================
FILE: pyproject.toml
================================================
[project]
name = "awesome-python"
version = "0.1.0"
description = "An opinionated guide to the best Python frameworks, libraries, and tools."
authors = [{ name = "Vinta Chen", email = "vinta.chen@gmail.com" }]
readme = "README.md"
license = "MIT"
requires-python = ">=3.14"
dependencies = []

[project.urls]
Homepage = "https://awesome-python.com/"
Repository = "https://github.com/vinta/awesome-python"

[dependency-groups]
build = ["httpx>=0.28.1", "jinja2>=3.1.6", "markdown-it-py>=4.2.0"]
lint = ["ruff>=0.16.10", "ty>=0.0.85"]
test = ["pytest>=9.1.1"]
preview = ["watchfiles>=1.3.0"]
dev = [
    { include-group = "build" },
    { include-group = "lint" },
    { include-group = "test" },
    { include-group = "preview" },
]

[tool.uv]
exclude-newer = "3 days"
no-build = true

[tool.uv.pip]
only-binary = [":all:"]

[tool.ruff]
line-length = 200
src = ["website"]

[tool.ty.environment]
python-version = "3.14"
root = ["website"]

[tool.ty.terminal]
error-on-warning = true

[tool.ty.rules]
division-by-zero = "error"
possibly-missing-attribute = "error"
possibly-missing-import = "error"
possibly-unresolved-reference = "error"
unused-ignore-comment = "error"

[tool.pytest.ini_options]
testpaths = ["website/tests"]
pythonpath = ["website"]



================================================
FILE: SPONSORSHIP.md
================================================
# Sponsor awesome-python

**The #10 most-starred repository on all of GitHub.**

awesome-python is where Python developers go to discover tools. It ranks on the first page of Google for "best Python libraries," is referenced by ChatGPT and other LLMs when recommending Python tools, and is the list developers check when evaluating frameworks.

Your sponsorship puts your product in front of developers at the exact moment they're choosing what to use.

## Audience

| Metric       | Value                                                                                                |
| ------------ | ---------------------------------------------------------------------------------------------------- |
| Stars        | ![Stars](https://img.shields.io/github/stars/vinta/awesome-python?style=for-the-badge)               |
| Forks        | ![Forks](https://img.shields.io/github/forks/vinta/awesome-python?style=for-the-badge)               |
| Watchers     | ![Watchers](https://img.shields.io/github/watchers/vinta/awesome-python?style=for-the-badge)         |
| Contributors | ![Contributors](https://img.shields.io/github/contributors/vinta/awesome-python?style=for-the-badge) |

**Who visits:** Professional Python developers evaluating libraries and tools for production use. Not beginners browsing tutorials. People making adoption decisions.

**Where they come from:** Google Search, GitHub, Reddit, YouTube, ChatGPT/LLMs, Hacker News.

## Sponsorship Tiers

### Headline Sponsor - $500/month or $4,500/year

- Large logo and one-line description (max 120 characters) pinned at the very top of the README, above all project entries
- Logo link in the sponsor section of [awesome-python.com](https://awesome-python.com/)

### Featured Sponsor - $200/month or $1,800/year

- Small logo and text entry (`[Name](URL) - Description.`, max 120 characters) pinned at the top of the README, directly below Headline sponsors
- Logo and text link in the sponsor section of [awesome-python.com](https://awesome-python.com/)

### Indie Dev Sponsor - $99/month, $249/quarter, or $891/year

- Lower-cost tier for indie developers, solo founders, and one-person companies only
- Text entry (`[Name](URL) - Description.`, max 120 characters) in the README sponsor section, directly below Featured sponsors
- Text link in the sponsor section of [awesome-python.com](https://awesome-python.com/)

Indie Dev Sponsor is available only to founder-led (one-person company) products. Funded startups, larger companies, and products with enterprise sales teams should use Featured or Headline Sponsor.

## Get Started

Email [sponsorship@awesome-python.com](mailto:sponsorship@awesome-python.com?subject=Awesome%20Python%20Sponsorship) with:

- **Tier:** Headline, Featured, or Indie Dev Sponsor
- **Content:** a `[Name](URL) - Description.` entry, plus a logo for Headline and Featured
- **Duration:** 1, 3, 6, or 12 months (a year gets 3 months free)
- **Payment method:** card via [Open Collective](https://opencollective.com/awesome-python), US bank transfer (ACH/wire), or PayPal

One upfront payment per term. Setup takes less than 24 hours.

Sponsor links carry UTM tags, so clicks show up in your own analytics as `awesome-python / sponsorship`.

## Previously Sponsored By

- [Warp](https://www.warp.dev/) - The terminal for modern developers.
- [pyr](https://pyrun.dev) - Zero-config Python project manager.

## Editorial Independence

Sponsorship is logo or link placement in the README header. It does not influence which projects are listed. Listings are curated on merit through the normal [contribution process](CONTRIBUTING.md).

We reserve the right to request changes to sponsor text, logos, or links that are misleading, off-topic, or incompatible with the README formatting.



================================================
FILE: uv.lock
================================================
version = 1
revision = 5
requires-python = ">=3.14"

[options]
exclude-newer = "0001-01-01T00:00:00Z" # This has no effect and is included for backwards compatibility when using relative exclude-newer values.
exclude-newer-span = "P3D"

[[package]]
name = "anyio"
version = "4.15.1"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "idna" },
    { name = "typing-extensions", marker = "python_full_version < '3.15'" },
]
sdist = { url = "https://files.pythonhosted.org/packages/a9/d2/f4d173e22df740bc37b1db102b386ba719b66e95b0f0d751f556b387e6d2/anyio-4.15.1.tar.gz", hash = "sha256:9f28306018cbd6d329e64a36d58256edff76dd996fe423bc957326e578b82a94", size = 276966, upload-time = "2026-09-05T10:42:39.44Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/12/b8/4bd346e22b28902df4d651910f5242c28d84e4a5c2435ca5c3f797ed7e2e/anyio-4.15.1-py3-none-any.whl", hash = "sha256:6152fdbbf9a77fdec97731721bebf7c4c44f7c29b424b0065826173efc7ed101", size = 132079, upload-time = "2026-09-05T10:42:37.923Z" },
]

[[package]]
name = "awesome-python"
version = "0.1.0"
source = { virtual = "." }

[package.dev-dependencies]
build = [
    { name = "httpx" },
    { name = "jinja2" },
    { name = "markdown-it-py" },
]
dev = [
    { name = "httpx" },
    { name = "jinja2" },
    { name = "markdown-it-py" },
    { name = "pytest" },
    { name = "ruff" },
    { name = "ty" },
    { name = "watchfiles" },
]
lint = [
    { name = "ruff" },
    { name = "ty" },
]
preview = [
    { name = "watchfiles" },
]
test = [
    { name = "pytest" },
]

[package.metadata]

[package.metadata.requires-dev]
build = [
    { name = "httpx", specifier = ">=0.28.1" },
    { name = "jinja2", specifier = ">=3.1.6" },
    { name = "markdown-it-py", specifier = ">=4.2.0" },
]
dev = [
    { name = "httpx", specifier = ">=0.28.1" },
    { name = "jinja2", specifier = ">=3.1.6" },
    { name = "markdown-it-py", specifier = ">=4.2.0" },
    { name = "pytest", specifier = ">=9.1.1" },
    { name = "ruff", specifier = ">=0.16.10" },
    { name = "ty", specifier = ">=0.0.85" },
    { name = "watchfiles", specifier = ">=1.3.0" },
]
lint = [
    { name = "ruff", specifier = ">=0.16.10" },
    { name = "ty", specifier = ">=0.0.85" },
]
preview = [{ name = "watchfiles", specifier = ">=1.3.0" }]
test = [{ name = "pytest", specifier = ">=9.1.1" }]

[[package]]
name = "certifi"
version = "2026.10.18"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/7e/eb/a2aa1ac3ea30dd3f30ca57f40232138b6b0040719316ecb85daf61167771/certifi-2026.10.18.tar.gz", hash = "sha256:b9995d97b64d0431a5af837d8ca8cd6238104d1f319f04bd93ea43124d6c861e", size = 135227, upload-time = "2026-10-18T16:21:07.655Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/08/ba/95dd616042484f7c83a06974388b37b837732740ee70bc5dc715b5fcd55a/certifi-2026.10.18-py3-none-any.whl", hash = "sha256:73191c47aaa79da394e8fee2dbc2ec827432cab56311122c9e47abf79e390f62", size = 134093, upload-time = "2026-10-18T16:21:06.276Z" },
]

[[package]]
name = "colorama"
version = "0.4.6"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/d8/53/6f443c9a4a8358a93a6792e2acffb9d9d5cb0a5cfd8802644b7b1c9a02e4/colorama-0.4.6.tar.gz", hash = "sha256:08695f5cb7ed6e0531a20572697297273c47b8cae5a63ffc6d6ed5c201be6e44", size = 27697, upload-time = "2022-10-25T02:36:22.414Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/d1/d6/3965ed04c63042e047cb6a3e6ed1a63a35087b6a609aa3a15ed8ac56c221/colorama-0.4.6-py2.py3-none-any.whl", hash = "sha256:4f1d9991f5acc0ca119f9d443620b77f9d6b33703e51011c16baf57afb285fc6", size = 25335, upload-time = "2022-10-25T02:36:20.889Z" },
]

[[package]]
name = "h11"
version = "0.16.0"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/01/ee/02a2c011bdab74c6fb3c75474d40b3052059d95df7e73351460c8588d963/h11-0.16.0.tar.gz", hash = "sha256:4e35b956cf45792e4caa5885e69fba00bdbc6ffafbfa020300e549b208ee5ff1", size = 101250, upload-time = "2025-04-24T03:35:25.427Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/04/4b/29cac41a4d98d144bf5f6d33995617b185d14b22401f75ca86f384e87ff1/h11-0.16.0-py3-none-any.whl", hash = "sha256:63cf8bbe7522de3bf65932fda1d9c2772064ffb3dae62d55932da54b31cb6c86", size = 37515, upload-time = "2025-04-24T03:35:24.344Z" },
]

[[package]]
name = "httpcore"
version = "1.0.9"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "certifi" },
    { name = "h11" },
]
sdist = { url = "https://files.pythonhosted.org/packages/06/94/82699a10bca87a5556c9c59b5963f2d039dbd239f25bc2a63907a05a14cb/httpcore-1.0.9.tar.gz", hash = "sha256:6e34463af53fd2ab5d807f399a9b45ea31c3dfa2276f15a2c3f00afff6e176e8", size = 85484, upload-time = "2025-04-24T22:06:22.219Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/7e/f5/f66802a942d491edb555dd61e3a9961140fd64c90bce1eafd741609d334d/httpcore-1.0.9-py3-none-any.whl", hash = "sha256:2d400746a40668fc9dec9810239072b40b4484b640a8c38fd654a024c7a1bf55", size = 78784, upload-time = "2025-04-24T22:06:20.566Z" },
]

[[package]]
name = "httpx"
version = "0.28.1"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "anyio" },
    { name = "certifi" },
    { name = "httpcore" },
    { name = "idna" },
]
sdist = { url = "https://files.pythonhosted.org/packages/b1/df/48c586a5fe32a0f01324ee087459e112ebb7224f646c0b5023f5e79e9956/httpx-0.28.1.tar.gz", hash = "sha256:75e98c5f16b0f35b567856f597f06ff2270a374470a5c2392242528e3e3e42fc", size = 141406, upload-time = "2024-12-06T15:37:23.222Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/2a/39/e50c7c3a983047577ee07d2a9e53faf5a69493943ec3f6a384bdc792deb2/httpx-0.28.1-py3-none-any.whl", hash = "sha256:d909fcccc110f8c7faf814ca82a9a4d816bc5a6dbfea25d6591d6985b8ba59ad", size = 73517, upload-time = "2024-12-06T15:37:21.509Z" },
]

[[package]]
name = "idna"
version = "3.20"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/f5/08/8eea9d4b8302028f3abb2c0813953f7aec26d33b7a8960ed760e65ff29fa/idna-3.20.tar.gz", hash = "sha256:a7db850025b95ded1eae8a46181a1a6c56c92c96f0e2b005d9ff8dc0210cab44", size = 216463, upload-time = "2026-09-17T14:11:04.752Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/58/a2/bb081bab032533a855d44de1d56f8e8426114ff1ba5d1f07a438a0a654f8/idna-3.20-py3-none-any.whl", hash = "sha256:ab7ae7122974553370f0bdb919e1a960b2cd1bc1ef0276416d896db81c14582c", size = 69583, upload-time = "2026-09-17T14:11:03.168Z" },
]

[[package]]
name = "iniconfig"
version = "2.3.1"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/01/e1/2069291243c926a2ff1cd706c7f3eeb9b62144bf60f77c9fb9ff2fb26bd3/iniconfig-2.3.1.tar.gz", hash = "sha256:67f4b9c50da0dedf52af349e7749a80a9057a5031199791b906c3bb3ae878960", size = 21209, upload-time = "2026-10-06T22:48:38.076Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/56/43/4ca9e49d27a1fcf6bece6f6aec0ea46bb9112489b93d4b688fb415457bdb/iniconfig-2.3.1-py3-none-any.whl", hash = "sha256:9121e2c1fdb355232495be3194c8dfe87ccc2d5dee45947b78e68f499790d7a7", size = 7552, upload-time = "2026-10-06T22:48:36.959Z" },
]

[[package]]
name = "jinja2"
version = "3.1.6"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "markupsafe" },
]
sdist = { url = "https://files.pythonhosted.org/packages/df/bf/f7da0350254c0ed7c72f3e33cef02e048281fec7ecec5f032d4aac52226b/jinja2-3.1.6.tar.gz", hash = "sha256:0137fb05990d35f1275a587e9aee6d56da821fc83491a0fb838183be43f66d6d", size = 245115, upload-time = "2025-03-05T20:05:02.478Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/62/a1/3d680cbfd5f4b8f15abc1d571870c5fc3e594bb582bc3b64ea099db13e56/jinja2-3.1.6-py3-none-any.whl", hash = "sha256:85ece4451f492d0c13c5dd7c13a64681a86afae63a5f347908daf103ce6d2f67", size = 134899, upload-time = "2025-03-05T20:05:00.369Z" },
]

[[package]]
name = "markdown-it-py"
version = "4.2.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "mdurl" },
]
sdist = { url = "https://files.pythonhosted.org/packages/06/ff/7841249c247aa650a76b9ee4bbaeae59370dc8bfd2f6c01f3630c35eb134/markdown_it_py-4.2.0.tar.gz", hash = "sha256:04a21681d6fbb623de53f6f364d352309d4094dd4194040a10fd51833e418d49", size = 82454, upload-time = "2026-05-07T12:08:28.36Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/b3/81/4da04ced5a082363ecfa159c010d200ecbd959ae410c10c0264a38cac0f5/markdown_it_py-4.2.0-py3-none-any.whl", hash = "sha256:9f7ebbcd14fe59494226453aed97c1070d83f8d24b6fc3a3bcf9a38092641c4a", size = 91687, upload-time = "2026-05-07T12:08:27.182Z" },
]

[[package]]
name = "markupsafe"
version = "3.0.4"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/38/9b/e422a865e1d5d57d0e509b4e0bf1c1a70a7f6382c29a5aa428df994c8bc8/markupsafe-3.0.4.tar.gz", hash = "sha256:2e9ad7dd851bf45fab9f75cbff4cb493fee9979e8d8c7c9c3ee119022518edd6", size = 153777, upload-time = "2026-10-02T23:07:22.29Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/5c/c3/a944f3b0df22bd129e96915b9f4e98d2eeca6516687d7618304a966c3c74/markupsafe-3.0.4-cp314-cp314-android_24_arm64_v8a.whl", hash = "sha256:4ed644d75aa94a2baf7ec3a96eaa160ea58c742eb9d27c6506053c5c40fc84ed", size = 12787, upload-time = "2026-10-02T23:05:30.971Z" },
    { url = "https://files.pythonhosted.org/packages/d4/d6/a44863f69d88b6c7e27889108f70d47aed259edf89d5df3c5fca1eac87d6/markupsafe-3.0.4-cp314-cp314-android_24_x86_64.whl", hash = "sha256:6d2a9efe686f9de00d0d1ea32a4a5a86d558a2277501bd78d964214eab625e59", size = 12525, upload-time = "2026-10-02T23:05:32.263Z" },
    { url = "https://files.pythonhosted.org/packages/17/8f/168ba80e532dd6a93f96f8f706f1ad41d7990b6e1aeedc1cc0d211a33497/markupsafe-3.0.4-cp314-cp314-ios_13_0_arm64_iphoneos.whl", hash = "sha256:8781a792a070cf2bd1b86d3aa943894115faaba6e88122a7bf32d62072742453", size = 11589, upload-time = "2026-10-02T23:05:33.251Z" },
    { url = "https://files.pythonhosted.org/packages/32/b3/aa2c95a574d3af39403a469b295886eb9b6d448da568cbebb5a2cbfdc2e5/markupsafe-3.0.4-cp314-cp314-ios_13_0_arm64_iphonesimulator.whl", hash = "sha256:971a3bbb75d97ae4e2e8f7d4834236f86f85f0c85e04ab2e191db1123b04f80b", size = 11801, upload-time = "2026-10-02T23:05:34.315Z" },
    { url = "https://files.pythonhosted.org/packages/60/d0/34b810107d83840e768bf485de795893ebbae35b26ab061b487adfa0a692/markupsafe-3.0.4-cp314-cp314-ios_13_0_x86_64_iphonesimulator.whl", hash = "sha256:8909c2f1c6dd65e054ac4b573a91c8384d1492281e55d82d159d653f7a13adf6", size = 11447, upload-time = "2026-10-02T23:05:35.302Z" },
    { url = "https://files.pythonhosted.org/packages/6c/ab/2f8488f0f817a39fca068d2b17daf446bf5cdb3eae28c3720af534d873b4/markupsafe-3.0.4-cp314-cp314-macosx_10_15_x86_64.whl", hash = "sha256:4cf3468d5ec187ffffcaca8e61929a37448f215dafc1386a12c750a72fe53634", size = 11722, upload-time = "2026-10-02T23:05:36.363Z" },
    { url = "https://files.pythonhosted.org/packages/ad/40/e2d117b048d47282ade906fbfd92814cbee5647afc13fda88a3406039372/markupsafe-3.0.4-cp314-cp314-macosx_11_0_arm64.whl", hash = "sha256:52704c5d36eb6dda8866493decd61111fff86244c9b1ad225ca01b9e91e5970f", size = 12061, upload-time = "2026-10-02T23:05:37.397Z" },
    { url = "https://files.pythonhosted.org/packages/9a/a8/73a81135e85ba66217f5af7facb03bbb386807e1a729ab64532e4c802652/markupsafe-3.0.4-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:1caa2fa5a6184fb233153b35f654e6687bd555476f6170f29d8ee9be1a8b0af9", size = 24434, upload-time = "2026-10-02T23:05:38.407Z" },
    { url = "https://files.pythonhosted.org/packages/ac/ca/fa9216dd01efee2dfdacafe7df32b4d0170fbac694b0c258a193d6e53999/markupsafe-3.0.4-cp314-cp314-manylinux2014_armv7l.manylinux_2_17_armv7l.manylinux_2_31_armv7l.whl", hash = "sha256:387d8cd30e69b3f0a72877b9ae717033396404e19095b17fe89753a981fda44f", size = 27183, upload-time = "2026-10-02T23:05:39.581Z" },
    { url = "https://files.pythonhosted.org/packages/fa/4e/a469509e538d37af51103b17b073126973f2b1cbf197ff32c7ddf025cfe5/markupsafe-3.0.4-cp314-cp314-manylinux2014_ppc64le.manylinux_2_17_ppc64le.manylinux_2_28_ppc64le.whl", hash = "sha256:051417f74bcaaefa316276e0ff723f541616ca51043d070da00249d9bddd3e3c", size = 24813, upload-time = "2026-10-02T23:05:40.671Z" },
    { url = "https://files.pythonhosted.org/packages/8f/db/d7282caf7ab03af44d5d6fdbaa019b35c7d7f1c90588b839c07cba640d6a/markupsafe-3.0.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:a8e9f292fcda89b324f2f5c91d13f1424a153e40fc2756f38ee23b15835ff300", size = 23049, upload-time = "2026-10-02T23:05:41.864Z" },
    { url = "https://files.pythonhosted.org/packages/30/f3/b6a425206e6964efda6acee544d0eb01d1501784d0b8e2dcc74986f33b17/markupsafe-3.0.4-cp314-cp314-manylinux_2_31_riscv64.manylinux_2_39_riscv64.whl", hash = "sha256:df1ae86ff54725a01fa1a0510b914ca53a161b7050be74f6204e24aded5971d0", size = 22088, upload-time = "2026-10-02T23:05:43.014Z" },
    { url = "https://files.pythonhosted.org/packages/ea/8a/84d3582fc1f0d5bd466cdf2eebf175e172158a6e70701aacec1de1b35430/markupsafe-3.0.4-cp314-cp314-musllinux_1_2_aarch64.whl", hash = "sha256:8965520ac587c94a4ac48b729be3d8b8de00af39699b17585dfb599babe77977", size = 23846, upload-time = "2026-10-02T23:05:44.098Z" },
    { url = "https://files.pythonhosted.org/packages/1c/65/db101cce51b7ba4864ac491a9859d297dd1adf0e55b103fee9db9c47c527/markupsafe-3.0.4-cp314-cp314-musllinux_1_2_armv7l.whl", hash = "sha256:340cbb1957ba99929cbf19a75626d36ba1ae21d1730b287d1cf7f824a20c4fc7", size = 22674, upload-time = "2026-10-02T23:05:45.23Z" },
    { url = "https://files.pythonhosted.org/packages/e0/49/ddee9813d71db0c7a5c9d97c832125e6758a0c844777f1cf076569bb0e22/markupsafe-3.0.4-cp314-cp314-musllinux_1_2_ppc64le.whl", hash = "sha256:3a93d9616ddecfb393727a0041a562cf0b15a244e20f2bd25efc7949be4c4f17", size = 24104, upload-time = "2026-10-02T23:05:46.398Z" },
    { url = "https://files.pythonhosted.org/packages/aa/0e/7d8518d726726870a2399d69fd30d0fa36c5e57a2132c336b58d7c491073/markupsafe-3.0.4-cp314-cp314-musllinux_1_2_riscv64.whl", hash = "sha256:d2e56fd3b00222722abfb3f5f0759ddbae4b90811b5ad4343c64030ad1bde70c", size = 21637, upload-time = "2026-10-02T23:05:47.48Z" },
    { url = "https://files.pythonhosted.org/packages/b4/b0/b505e8a361ba557dbf3b3aa7331ea39b00d2022a26e925ff8463b9714bb3/markupsafe-3.0.4-cp314-cp314-musllinux_1_2_x86_64.whl", hash = "sha256:0d9c47709875fdb321452056622e930c52afbc07a7d780762fbb8b4d91ce6fa4", size = 23081, upload-time = "2026-10-02T23:05:48.611Z" },
    { url = "https://files.pythonhosted.org/packages/1c/ea/9cc3cea873f980c75cbdb6f4277ce30ee955de38be0b3d02f14c108e0698/markupsafe-3.0.4-cp314-cp314-win32.whl", hash = "sha256:38fc55594dab834470b6733dead2ee9e3f657fb0608c769dcafa0ba5ab52f45c", size = 14272, upload-time = "2026-10-02T23:05:49.707Z" },
    { url = "https://files.pythonhosted.org/packages/80/f0/5792ff768a410f93ee3f84fc19345295ffc352d2c936b424cb37e514714c/markupsafe-3.0.4-cp314-cp314-win_amd64.whl", hash = "sha256:c1bc67752d5f21013cfe430df4062441714eab79f65a6a05e01505957e9c35fe", size = 14501, upload-time = "2026-10-02T23:05:50.788Z" },
    { url = "https://files.pythonhosted.org/packages/5f/cf/3d074a8edffcc6899355232ff2543ae8d929733239596423b7db79698bc9/markupsafe-3.0.4-cp314-cp314-win_arm64.whl", hash = "sha256:7e1636da3d8dfc220b6dd10264db5f2b165e4888c4518594898fbe381049af8a", size = 14364, upload-time = "2026-10-02T23:05:51.857Z" },
    { url = "https://files.pythonhosted.org/packages/d9/31/87ce42159aae2163cf3bbbd0c44bc87780510eecab1ea3859099aed95dcb/markupsafe-3.0.4-cp314-cp314t-macosx_10_15_x86_64.whl", hash = "sha256:805c8b84534fa10891890f0e4be39f3a99e94615d93e8836bf9fa1fdca2feeb2", size = 11759, upload-time = "2026-10-02T23:05:52.951Z" },
    { url = "https://files.pythonhosted.org/packages/5f/53/b047207eeb7752e960aca3eb1df5fb7eefa7dd4c62ac49bb156456c8a702/markupsafe-3.0.4-cp314-cp314t-macosx_11_0_arm64.whl", hash = "sha256:fa95848c929b6a75f6848d3c9793e59db365ee436776e57db835cdbfa79ba977", size = 12096, upload-time = "2026-10-02T23:05:54.066Z" },
    { url = "https://files.pythonhosted.org/packages/ee/51/4326c88a13c7b755657d44b4bb986f8c3d9843ecba7e22d98661d87f9a57/markupsafe-3.0.4-cp314-cp314t-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:e916035e3e9930cbdfdd10abf48861340221857f45509565898e012263f7b289", size = 25699, upload-time = "2026-10-02T23:05:55.15Z" },
    { url = "https://files.pythonhosted.org/packages/f2/bb/990581b7474bfcf2cf34bed6ba5ea23bd87adb9d671213d68e88620e7a6b/markupsafe-3.0.4-cp314-cp314t-manylinux2014_armv7l.manylinux_2_17_armv7l.manylinux_2_31_armv7l.whl", hash = "sha256:b4d12837e0203bbace818ff4a7461afdcd78bcd782351cea148139180d7bcffe", size = 27804, upload-time = "2026-10-02T23:05:56.29Z" },
    { url = "https://files.pythonhosted.org/packages/6b/89/89491878c28e8291f5aa2fffe2c2d57230d10ae366d55dd810b840513d78/markupsafe-3.0.4-cp314-cp314t-manylinux2014_ppc64le.manylinux_2_17_ppc64le.manylinux_2_28_ppc64le.whl", hash = "sha256:5086f9975abb1ab531ee6afca1761e4b59a19b446f3f6522ed776963228cfe5a", size = 25912, upload-time = "2026-10-02T23:05:57.416Z" },
    { url = "https://files.pythonhosted.org/packages/30/77/680998b54efdea06fc114565cd739b6d059f826a0279219b218dfa750d29/markupsafe-3.0.4-cp314-cp314t-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:b4a635a0487774f841cb1fb62e907e7195cc95bc761e053184b8acc3ceb20733", size = 23623, upload-time = "2026-10-02T23:05:58.557Z" },
    { url = "https://files.pythonhosted.org/packages/ae/75/2709f5ac5de9467b40b10e2bb8f89cc63dfb74582e09aa734b1124a217de/markupsafe-3.0.4-cp314-cp314t-manylinux_2_31_riscv64.manylinux_2_39_riscv64.whl", hash = "sha256:cb96e6e088d6cf71c1ea977510948320234824cf226e32f6f6e044f7a9c82b34", size = 23301, upload-time = "2026-10-02T23:05:59.94Z" },
    { url = "https://files.pythonhosted.org/packages/a0/c8/39eadc6c5b14c9c7679bfb98f4d4c6a97863b5beb91839aca4d2d6e16e55/markupsafe-3.0.4-cp314-cp314t-musllinux_1_2_aarch64.whl", hash = "sha256:8b5d563170ff8ba3181caa967c99a3c804d1dedb702c7cb93a6a7c32247da978", size = 24950, upload-time = "2026-10-02T23:06:01.289Z" },
    { url = "https://files.pythonhosted.org/packages/1a/5e/01037f8a43e8ccb0bffb4fbdc5212db05bf080fdd7286cd392332d58128a/markupsafe-3.0.4-cp314-cp314t-musllinux_1_2_armv7l.whl", hash = "sha256:396ec4e65cc889f69786b3b89478b471cee5a3bcf468b9d9bb03e1a30fb291fc", size = 23330, upload-time = "2026-10-02T23:06:02.441Z" },
    { url = "https://files.pythonhosted.org/packages/d4/f4/23e83ce0596bb0cbe670502d31df8f757bbd01a392aa486fa3b40d1ed399/markupsafe-3.0.4-cp314-cp314t-musllinux_1_2_ppc64le.whl", hash = "sha256:15ba9e28640feef770374b116a6f019c21f52404aeabe516aa7f800587b98cfc", size = 25239, upload-time = "2026-10-02T23:06:03.579Z" },
    { url = "https://files.pythonhosted.org/packages/88/5b/3708897368073cc683d524750474f41a77d2986152c380dcc55b20fdf340/markupsafe-3.0.4-cp314-cp314t-musllinux_1_2_riscv64.whl", hash = "sha256:d920abdfa61279ba1a2ef9484aab07bf03331f8c08a10120fa332353d06e6932", size = 22767, upload-time = "2026-10-02T23:06:04.699Z" },
    { url = "https://files.pythonhosted.org/packages/c6/61/ebda1307864b409e6b3115757a3d4a09cca46cfb6cc65191b5de226b424b/markupsafe-3.0.4-cp314-cp314t-musllinux_1_2_x86_64.whl", hash = "sha256:a9f54054101545a9a9cccefddf54316aa6e4491611fcbef9e91b3b6bebec04f6", size = 23668, upload-time = "2026-10-02T23:06:05.9Z" },
    { url = "https://files.pythonhosted.org/packages/09/15/98075cceac3b5ba0dbb8e4762a847be967d2befc349a2cf2d0ac77f62c9d/markupsafe-3.0.4-cp314-cp314t-win32.whl", hash = "sha256:12a606a492de952afcb43b59a14aaaaad120e708d3663dd0fdf2d738d427a691", size = 14301, upload-time = "2026-10-02T23:06:07.109Z" },
    { url = "https://files.pythonhosted.org/packages/0b/a3/768b560fcc4156685cb563d922b217810cfa7bc135773367f62f1f9d2078/markupsafe-3.0.4-cp314-cp314t-win_amd64.whl", hash = "sha256:a18f38cafc329bac5e3c2b96c765b4c96d3d103421ed22ab7988c1e3fce27464", size = 14526, upload-time = "2026-10-02T23:06:08.276Z" },
    { url = "https://files.pythonhosted.org/packages/93/63/da554b4c97a6b0ea3229ca7fe8cbfb620be81613d517f482e85958550537/markupsafe-3.0.4-cp314-cp314t-win_arm64.whl", hash = "sha256:eba154571c16e032112afac0dc2dfe9e63c2ceb7aedd07bb7eecf2ce26d4dd4c", size = 14421, upload-time = "2026-10-02T23:06:09.402Z" },
    { url = "https://files.pythonhosted.org/packages/a9/30/54d11c8ca027114898cab97421fb39e4ffd9ddf47cdbc44df2ec76722da9/markupsafe-3.0.4-cp315-cp315-android_24_arm64_v8a.whl", hash = "sha256:737c9c3981998eba27f11786f84fddcbabc74068b72a4a1f454ea02094b57b65", size = 12791, upload-time = "2026-10-02T23:06:10.485Z" },
    { url = "https://files.pythonhosted.org/packages/10/6d/97c913e253a14bd3cd0e15a5c56d13203b823fa7ee32498342896a072dc4/markupsafe-3.0.4-cp315-cp315-android_24_x86_64.whl", hash = "sha256:489505b03f692c3f376394e49194fa7a7f9e8558d6e293a7056a0032b0c38163", size = 12527, upload-time = "2026-10-02T23:06:11.834Z" },
    { url = "https://files.pythonhosted.org/packages/26/f9/b86d032042a4d597d9e1997f0e5f63a3eedaf11258e0a05760b0a0a826ea/markupsafe-3.0.4-cp315-cp315-ios_13_0_arm64_iphoneos.whl", hash = "sha256:077293e425f28ec737dbcad442a71752e28f8ae27cde3d68acd1fb212091cd92", size = 11602, upload-time = "2026-10-02T23:06:13.122Z" },
    { url = "https://files.pythonhosted.org/packages/f2/dc/73c14c1eedf0ac5fa3292ba43435e6c49d2c2050f33cebde541f8f4807f1/markupsafe-3.0.4-cp315-cp315-ios_13_0_arm64_iphonesimulator.whl", hash = "sha256:9348cbb300d224fe3b89793262cb093504d4ae927004468463f745188a193e4a", size = 11817, upload-time = "2026-10-02T23:06:14.227Z" },
    { url = "https://files.pythonhosted.org/packages/8f/69/2c2fcaa5fcee22d72c7819c0d536fd181c74a688e6143845419579cd2863/markupsafe-3.0.4-cp315-cp315-ios_13_0_x86_64_iphonesimulator.whl", hash = "sha256:b807e598953730f82e4eae3bd30f6a122cf6b31c398c6b504c0e04c13c170429", size = 11446, upload-time = "2026-10-02T23:06:15.574Z" },
    { url = "https://files.pythonhosted.org/packages/88/54/9e5ec76c62e6e2834d5a93623018c943e8b3bb41d663e3fd4c03303b9b85/markupsafe-3.0.4-cp315-cp315-macosx_10_15_x86_64.whl", hash = "sha256:799c39bdf5e2f1292fedd3009f7b3c9e760f10b2420cb9638d56920840ff6db8", size = 11719, upload-time = "2026-10-02T23:06:16.701Z" },
    { url = "https://files.pythonhosted.org/packages/96/24/3ec292b44064c16229e064d770b2625bd8ea941aa61f44905a9fa44942c0/markupsafe-3.0.4-cp315-cp315-macosx_11_0_arm64.whl", hash = "sha256:ae9dcb8fbe244cb82f8a6458b455b927a03685e383d9bacf1ea5ce180b96dc97", size = 12075, upload-time = "2026-10-02T23:06:17.855Z" },
    { url = "https://files.pythonhosted.org/packages/aa/85/b64fdb1f304848518742136983c24e96d967bfb59a0ea160e92736901ab0/markupsafe-3.0.4-cp315-cp315-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:4bced6e2a6dba6a28f7dd3c6ce14df1b2dd495923f16ea484cad03decd463b2b", size = 24656, upload-time = "2026-10-02T23:06:18.963Z" },
    { url = "https://files.pythonhosted.org/packages/9c/18/23997d4c65b355da6390d61cd56e0ab3befd6ba8dda25cb40c602bd0fa6b/markupsafe-3.0.4-cp315-cp315-manylinux2014_armv7l.manylinux_2_17_armv7l.manylinux_2_31_armv7l.whl", hash = "sha256:3882fb412298575bae3b9c46868251f15cc69307359f87bb1b382e53d6e5a2c9", size = 27737, upload-time = "2026-10-02T23:06:20.117Z" },
    { url = "https://files.pythonhosted.org/packages/d4/36/35998dead3c6af88c38265a56e58100211f036234ab88eb2283fd4cbce44/markupsafe-3.0.4-cp315-cp315-manylinux2014_ppc64le.manylinux_2_17_ppc64le.manylinux_2_28_ppc64le.whl", hash = "sha256:04e7902ba80ee4bac1d50a549606527a1dcf0476cd81403db41099d3b60ec653", size = 25003, upload-time = "2026-10-02T23:06:21.284Z" },
    { url = "https://files.pythonhosted.org/packages/82/96/ef49135ce260db4ca4a12b119ed468449cd248db6b1468e2112b546d7a2e/markupsafe-3.0.4-cp315-cp315-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:925f929d6b59a8b3f8b8c6ac363cd0af7eecc81efb3071770b3c6717c450a369", size = 23111, upload-time = "2026-10-02T23:06:22.524Z" },
    { url = "https://files.pythonhosted.org/packages/50/7d/83126e338bd88c17a220668235368ad719fd4638e426739858cbb8508f77/markupsafe-3.0.4-cp315-cp315-manylinux_2_31_riscv64.manylinux_2_39_riscv64.whl", hash = "sha256:f68edfc67aabac33708941f26f22a7b8e9f81429bc0cf249fcf7d66b23af8d19", size = 22403, upload-time = "2026-10-02T23:06:23.785Z" },
    { url = "https://files.pythonhosted.org/packages/83/dd/daf7e420de23c8206c365204e7b85e1251d8e19d34196a56336f316e5ed2/markupsafe-3.0.4-cp315-cp315-musllinux_1_2_aarch64.whl", hash = "sha256:e5c802729725bd07e2bc3ab7b76dc7e0bbfc53129d8f1eb1c002c24cf774717e", size = 24083, upload-time = "2026-10-02T23:06:25.037Z" },
    { url = "https://files.pythonhosted.org/packages/19/3c/11eecdc06bc44ad5570350085b572ebf049e8f9a38d1ece6d76640b739cd/markupsafe-3.0.4-cp315-cp315-musllinux_1_2_armv7l.whl", hash = "sha256:55ffd6ce583d97dc71dc92e930324c8c0d25aea7e3ade6ae54ef77cedb096811", size = 22931, upload-time = "2026-10-02T23:06:26.328Z" },
    { url = "https://files.pythonhosted.org/packages/0d/9e/ac0fd77f2a726e56ecc3ca0235d095feace1358d1b822406c2a2ef26a4dc/markupsafe-3.0.4-cp315-cp315-musllinux_1_2_ppc64le.whl", hash = "sha256:2cb3dd71fc6be918ad4264346a8ed69485f9b7ed7bf35495d8e22807cd6b8bea", size = 24299, upload-time = "2026-10-02T23:06:27.742Z" },
    { url = "https://files.pythonhosted.org/packages/d7/09/c6bd842ad58ff5b3bc76eeed7e9a42a6f11adc5d090ec697b72c9672731e/markupsafe-3.0.4-cp315-cp315-musllinux_1_2_riscv64.whl", hash = "sha256:94f5407f7bc64fa6463906b896f9904beeeb7dd8dc116ee8e9056c8714ff9916", size = 21948, upload-time = "2026-10-02T23:06:29.274Z" },
    { url = "https://files.pythonhosted.org/packages/a3/46/82f586711fed61e86faa1ee1bc317d68cd45a10c8bdbe3f7d1fdf9026ad8/markupsafe-3.0.4-cp315-cp315-musllinux_1_2_x86_64.whl", hash = "sha256:2dad610540cb2e6272855c178f08ae9a1c7ac258a7fb71660553a5f104b42741", size = 23150, upload-time = "2026-10-02T23:06:30.583Z" },
    { url = "https://files.pythonhosted.org/packages/19/2d/2dfdce99318abbfa26925195fbc17db188c46a1ec6457be121b6f9cfeb42/markupsafe-3.0.4-cp315-cp315-win32.whl", hash = "sha256:03470d1a8268e692ecf79ecd565593e59d44219377a7ead61f1f1b94c1f7ff6b", size = 14269, upload-time = "2026-10-02T23:06:31.949Z" },
    { url = "https://files.pythonhosted.org/packages/5b/ec/6000fd82e8791e58fcd0456ec20f098957e2b03d5ed02eb73241a577c0ba/markupsafe-3.0.4-cp315-cp315-win_amd64.whl", hash = "sha256:d882a373d8093c2941e01291b7ced96e9cbe4781da9a7751ca7e6c70385e5214", size = 14496, upload-time = "2026-10-02T23:06:33.258Z" },
    { url = "https://files.pythonhosted.org/packages/bc/66/e73bd5016421d5d6e2fb6de7dd609f9de020942ac8c626526bd8c6eeaf82/markupsafe-3.0.4-cp315-cp315-win_arm64.whl", hash = "sha256:353bd63081912ab8cfa6a0c7d185934cdf8426f04c618bba6bc4b394f2069b67", size = 14361, upload-time = "2026-10-02T23:06:34.539Z" },
    { url = "https://files.pythonhosted.org/packages/90/df/cb8c3dc98d313a951df2f8968f44e4cb5643df6d3cab749a530ce2f7d972/markupsafe-3.0.4-cp315-cp315t-macosx_10_15_x86_64.whl", hash = "sha256:c61750fadcd119d0825bcb7d7d675dd264dcc89cc05292aab5be68ebdbb374ad", size = 11760, upload-time = "2026-10-02T23:06:35.807Z" },
    { url = "https://files.pythonhosted.org/packages/d6/bb/4af9b3ca0753d654ac75f9531d5bd741bb77ca6e696f36807c475ffc099a/markupsafe-3.0.4-cp315-cp315t-macosx_11_0_arm64.whl", hash = "sha256:1c0df495a977d10460a94941799c72d5b5ab03d3858d949b55b5a66c8f371c99", size = 12108, upload-time = "2026-10-02T23:06:37.089Z" },
    { url = "https://files.pythonhosted.org/packages/3f/d4/b56429313aee5fd59b079c3df5615299959e25e7113eb6d8caadbdd7d38a/markupsafe-3.0.4-cp315-cp315t-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:02fa4acbc6a3fc5c693c34d4dd8c1130b7fe99cc915181b0ddd6f72aeb296002", size = 25762, upload-time = "2026-10-02T23:06:38.419Z" },
    { url = "https://files.pythonhosted.org/packages/65/f5/34c181e891aa4f7d59c918584672e0c5eb7fffe76c1387d1246008bf4081/markupsafe-3.0.4-cp315-cp315t-manylinux2014_armv7l.manylinux_2_17_armv7l.manylinux_2_31_armv7l.whl", hash = "sha256:05295589e619b9bed252a86b532b8e27350abc372d18ba89b59375325e91ec1e", size = 28400, upload-time = "2026-10-02T23:06:39.819Z" },
    { url = "https://files.pythonhosted.org/packages/ce/b5/ad14694fd0ac9a5ce30bc6498f2999378f418583dd1679cca5a1b512957e/markupsafe-3.0.4-cp315-cp315t-manylinux2014_ppc64le.manylinux_2_17_ppc64le.manylinux_2_28_ppc64le.whl", hash = "sha256:be6cb0c799abb0e2ba3e618e6d28ddddf7e485f6c2ce938dfa237daf3905072c", size = 25946, upload-time = "2026-10-02T23:06:41.381Z" },
    { url = "https://files.pythonhosted.org/packages/d6/a8/26b606445387d0ceb1eb1f21840094b84e4e3c3c3983d80d10b89823b490/markupsafe-3.0.4-cp315-cp315t-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:26e9867520db70d37f7fb421a7f0d8adb40171011fb84ce869afa1a83370dfa8", size = 23634, upload-time = "2026-10-02T23:06:42.748Z" },
    { url = "https://files.pythonhosted.org/packages/39/a2/b8814de672f1f0094d498bf646f2fec9d6356b503d28ef500b71c5095377/markupsafe-3.0.4-cp315-cp315t-manylinux_2_31_riscv64.manylinux_2_39_riscv64.whl", hash = "sha256:f03460ff076f70ab595bb45a0205ccea1971443575b6920c52e755dec2b3fbfe", size = 23488, upload-time = "2026-10-02T23:06:44.176Z" },
    { url = "https://files.pythonhosted.org/packages/db/c7/287223376fb73335a3cc5d6eb22c6ab01358cf33945a9c39c06b9dac3f4b/markupsafe-3.0.4-cp315-cp315t-musllinux_1_2_aarch64.whl", hash = "sha256:436e3ffc6310d3c41878c601db29098102fe5d8a467c49da4a4125254e0980f2", size = 25037, upload-time = "2026-10-02T23:06:45.646Z" },
    { url = "https://files.pythonhosted.org/packages/f9/29/4df8355e313426d19e62ba33e0253c009ca12a0894ee77d67fa67255361c/markupsafe-3.0.4-cp315-cp315t-musllinux_1_2_armv7l.whl", hash = "sha256:4e2c4809c14559aa7ef426f27fb35afbb38104c349a903bf8f3600456764bb38", size = 23543, upload-time = "2026-10-02T23:06:47.264Z" },
    { url = "https://files.pythonhosted.org/packages/71/e5/8377731e8495668dcc768f645e717df18318c841edaf023a99395f6da9b4/markupsafe-3.0.4-cp315-cp315t-musllinux_1_2_ppc64le.whl", hash = "sha256:da2af0d7aebfc2074080d72efa6ab8317c62481ef1f896f65d9999c1c01f4494", size = 25282, upload-time = "2026-10-02T23:06:48.795Z" },
    { url = "https://files.pythonhosted.org/packages/ed/5f/373456e37ceb1478d657d6fe769cbe0a39f0a8dfc1548eeb19c471eefdd9/markupsafe-3.0.4-cp315-cp315t-musllinux_1_2_riscv64.whl", hash = "sha256:aa2c838cc024642cc04c6854232f32b43e5e22833dd11119c1766c7873b8370d", size = 22993, upload-time = "2026-10-02T23:06:50.31Z" },
    { url = "https://files.pythonhosted.org/packages/d7/93/2cbd5628435afb6f541bbaced4bce0c2edac4b09a142e6e928b8b0da9858/markupsafe-3.0.4-cp315-cp315t-musllinux_1_2_x86_64.whl", hash = "sha256:b91cc9d336957239ff200f30097e6fea2dc6d6fb3c81e853eaa09eac904fd894", size = 23712, upload-time = "2026-10-02T23:06:51.759Z" },
    { url = "https://files.pythonhosted.org/packages/81/99/157e10966b033b363aeda5263e82596ee232a0b1d082fdbf90aa417ff083/markupsafe-3.0.4-cp315-cp315t-win32.whl", hash = "sha256:e49fb0d1ce92cfa0cb198cc5b1b11cdf9d0638658e2a2db2687e39db7c87fc78", size = 14300, upload-time = "2026-10-02T23:06:53.241Z" },
    { url = "https://files.pythonhosted.org/packages/33/05/55884815414c9706a23deca150b72c25a62109e65b0b6ce232077802c719/markupsafe-3.0.4-cp315-cp315t-win_amd64.whl", hash = "sha256:4f6e0852a0283b1b1fd776eeb7b766a5f440b3e2bd31ab51af3b400585f3965c", size = 14522, upload-time = "2026-10-02T23:06:54.729Z" },
    { url = "https://files.pythonhosted.org/packages/92/f9/ecbde7149e95b8a0f18e16d5d747f7dc06049d5da2e4f77f6f5e4a1f46a8/markupsafe-3.0.4-cp315-cp315t-win_arm64.whl", hash = "sha256:39dbacefc411633db5b4378b066a9aca70a3d7e2922c9e578d825f844026eeba", size = 14417, upload-time = "2026-10-02T23:06:56.246Z" },
]

[[package]]
name = "mdurl"
version = "0.1.2"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/d6/54/cfe61301667036ec958cb99bd3efefba235e65cdeb9c84d24a8293ba1d90/mdurl-0.1.2.tar.gz", hash = "sha256:bb413d29f5eea38f31dd4754dd7377d4465116fb207585f97bf925588687c1ba", size = 8729, upload-time = "2022-08-14T12:40:10.846Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/b3/38/89ba8ad64ae25be8de66a6d463314cf1eb366222074cfda9ee839c56a4b4/mdurl-0.1.2-py3-none-any.whl", hash = "sha256:84008a41e51615a49fc9966191ff91509e3c40b939176e643fd50a5c2196b8f8", size = 9979, upload-time = "2022-08-14T12:40:09.779Z" },
]

[[package]]
name = "packaging"
version = "26.3"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/7d/fa/3944b40b07da9ce895c0e6303a5ab7d53da063554f534556b134a54d6093/packaging-26.3.tar.gz", hash = "sha256:94edc256424af38762eb31306eed28beb9f0efc50a8837492c9d6fd6004aed79", size = 313412, upload-time = "2026-08-04T18:15:28.737Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/63/34/ba1c580383c9eada3711951fef0795c80b829a078d72188184bcab9dd527/packaging-26.3-py3-none-any.whl", hash = "sha256:d7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c", size = 129956, upload-time = "2026-08-04T18:15:27.159Z" },
]

[[package]]
name = "pluggy"
version = "1.6.0"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/f9/e2/3e91f31a7d2b083fe6ef3fa267035b518369d9511ffab804f839851d2779/pluggy-1.6.0.tar.gz", hash = "sha256:7dcc130b76258d33b90f61b658791dede3486c3e6bfb003ee5c9bfb396dd22f3", size = 69412, upload-time = "2025-05-15T12:30:07.975Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/54/20/4d324d65cc6d9205fabedc306948156824eb9f0ee1633355a8f7ec5c66bf/pluggy-1.6.0-py3-none-any.whl", hash = "sha256:e920276dd6813095e9377c0bc5566d94c932c33b27a3e3945d8389c374dd4746", size = 20538, upload-time = "2025-05-15T12:30:06.134Z" },
]

[[package]]
name = "pygments"
version = "2.21.0"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/49/2e/ced460408999b33da6b31b0021b0f37d329e202d4169aeb164493778f25b/pygments-2.21.0.tar.gz", hash = "sha256:610ca751c9bc2492b38eb9a38a7fbc93edbbb2d7182edaf34e66ae493dee5c8c", size = 5005329, upload-time = "2026-08-17T08:02:48.824Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/71/46/17f022dd3e953bf20a04a028a21ec746d942f8d2af30fa0f124fa0e6a684/pygments-2.21.0-py3-none-any.whl", hash = "sha256:2363c69b61c4a97c838da3b130dcd6468f4848992b21a82f2a63ec34377137d9", size = 1250147, upload-time = "2026-08-17T08:02:44.912Z" },
]

[[package]]
name = "pytest"
version = "9.1.1"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "colorama", marker = "sys_platform == 'win32'" },
    { name = "iniconfig" },
    { name = "packaging" },
    { name = "pluggy" },
    { name = "pygments" },
]
sdist = { url = "https://files.pythonhosted.org/packages/e4/47/b9efed96c114afcfa3c9d3fe98a76a1d14c74a9e266d397cf6eb64be5e01/pytest-9.1.1.tar.gz", hash = "sha256:1088fbde8f2b49d95a549a195707afa7a76a3ce9bcadc26b6d71f0ffda5fe313", size = 1636369, upload-time = "2026-06-19T10:58:32.857Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/24/25/1de2678b631f5a49215c6c96fff41ba892b0a34df68d6d80292b1b48aa7f/pytest-9.1.1-py3-none-any.whl", hash = "sha256:37a86b45efb9a47a61a36449063e8e18d0cab3161329fc099eb21783169c4f0c", size = 386536, upload-time = "2026-06-19T10:58:31.347Z" },
]

[[package]]
name = "ruff"
version = "0.16.10"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/c4/49/23802c45f093eb14bde54b141d2b2f058edfa63a06db7beed047308cc08f/ruff-0.16.10.tar.gz", hash = "sha256:eff4728c4eaae93f0955cd264d24b2ab348e74bf59986ccf282ba6dc16b3b017", size = 4958724, upload-time = "2026-10-01T18:03:21.697Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/2f/21/ebce22e1d90cdb2cd691026b9c6e9bec6499f0b396089481755b5d49efff/ruff-0.16.10-py3-none-linux_armv6l.whl", hash = "sha256:488b0fe3f3574210e5cf80d9f59b9e3ab17a127a8155de3f307b392589cfb511", size = 10095557, upload-time = "2026-10-01T18:02:36.072Z" },
    { url = "https://files.pythonhosted.org/packages/cb/98/a54de85876a8b2612bfa0d84c7b9abfb39c6a3354aee7800b09c1649b9e3/ruff-0.16.10-py3-none-macosx_10_12_x86_64.whl", hash = "sha256:e748ff95c934c4e978783b8e687bc174e7bd84e8ad24e3243e1ecfcda5e0282d", size = 10340577, upload-time = "2026-10-01T18:02:39.258Z" },
    { url = "https://files.pythonhosted.org/packages/9f/16/1a5a4a2657effe4806110f2b907313802f1367fcdbb29e8122766e407fab/ruff-0.16.10-py3-none-macosx_11_0_arm64.whl", hash = "sha256:3031a4a2e8e7b8a46f70be45f198c35a11ece509a94b80334d8d397a33c67550", size = 9774282, upload-time = "2026-10-01T18:02:41.79Z" },
    { url = "https://files.pythonhosted.org/packages/6e/fb/470085af734da396e68cd80fb0a3e7c109a459716ae59588c0f6fab8a17d/ruff-0.16.10-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:494401c86df4c4c25f69b9419605d944467ee98c42fb6ad405ef4fa40b8fb67d", size = 9920895, upload-time = "2026-10-01T18:02:44.458Z" },
    { url = "https://files.pythonhosted.org/packages/57/de/f10cffe4f88a37ea6615ec460f01bf76f0bc1477737a35d9ee61a630a78b/ruff-0.16.10-py3-none-manylinux_2_17_armv7l.manylinux2014_armv7l.whl", hash = "sha256:d203abc0ff2b773ee33d00ab8df0bb67046fbc7c07b119332f08b9b345cf8221", size = 9902707, upload-time = "2026-10-01T18:02:47.041Z" },
    { url = "https://files.pythonhosted.org/packages/ff/44/3fdcedf83ae60ef837dd239170e480dce606a9142cfa2db911afdf855fd9/ruff-0.16.10-py3-none-manylinux_2_17_i686.manylinux2014_i686.whl", hash = "sha256:bd83d1235a5258d318477bc5b576303974cbdef5df0c01a1bff14efcc23bd12a", size = 10619287, upload-time = "2026-10-01T18:02:49.485Z" },
    { url = "https://files.pythonhosted.org/packages/c1/62/02e76a5574002153618eafbb70e159468addc72a5d2c488e65cbb4639d2d/ruff-0.16.10-py3-none-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl", hash = "sha256:bc2610fb269fa56dd8a68669ae470fa6272902668c0fc2ebc3aa112b2633d5b8", size = 11339942, upload-time = "2026-10-01T18:02:52.008Z" },
    { url = "https://files.pythonhosted.org/packages/6b/c4/cde27d47ad8d4126c587e608c67c46e7feac11763f606d261a1bc8a489e6/ruff-0.16.10-py3-none-manylinux_2_17_s390x.manylinux2014_s390x.whl", hash = "sha256:3e70175e29cc94c26ea296c80e470180b744b7419026898e58f520c6ab32578e", size = 10934316, upload-time = "2026-10-01T18:02:54.811Z" },
    { url = "https://files.pythonhosted.org/packages/e4/03/17234145f302a645a123e8c3bb2411ecf4669fbc350de3b0d803230a1729/ruff-0.16.10-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:f33f43a864a8483eebd160e713336c8bab02c934feaff0a33cf5ccb41546d09a", size = 10387968, upload-time = "2026-10-01T18:02:57.497Z" },
    { url = "https://files.pythonhosted.org/packages/71/29/2493af60240ee7644b38a4b821f5f9c3b5a4fa3178770fe1d0c685217395/ruff-0.16.10-py3-none-manylinux_2_31_riscv64.whl", hash = "sha256:1dfc6f0088149fb6a362c1c446bcbb3fd2157b3852fe2fa68409276eab9ad9b3", size = 10537906, upload-time = "2026-10-01T18:03:00.006Z" },
    { url = "https://files.pythonhosted.org/packages/2e/9a/f56b28f3b143bb9e518c34fb89ab191b626bca8b70dbf8af0d2e2d473572/ruff-0.16.10-py3-none-musllinux_1_2_aarch64.whl", hash = "sha256:6553498afc35f580f036030795810b9e6bcea31604b0fd9e8d352795473042e3", size = 10012938, upload-time = "2026-10-01T18:03:03.006Z" },
    { url = "https://files.pythonhosted.org/packages/c2/c4/fca37362848ea4d4d80712df13632e645e7c7cfb1bdedf140699ac7a090b/ruff-0.16.10-py3-none-musllinux_1_2_armv7l.whl", hash = "sha256:a3b8471dea115d37f123882be852bed13403746d3a76c11de4a19ec5f9ff5a03", size = 9897945, upload-time = "2026-10-01T18:03:05.818Z" },
    { url = "https://files.pythonhosted.org/packages/7d/c7/e0bc57664d6e0c61fd22f620af260fe9662d7e1ddb320ea7f160e76ef165/ruff-0.16.10-py3-none-musllinux_1_2_i686.whl", hash = "sha256:92e59a70bcbd9d3a5483656da906ec28edfdacfce00afd99edb8b4e9d15644be", size = 10333134, upload-time = "2026-10-01T18:03:08.25Z" },
    { url = "https://files.pythonhosted.org/packages/21/aa/5c9f3b68737c0e4a33a1db5dfab44f7b786d96ca91a7233112ddab1e6dc2/ruff-0.16.10-py3-none-musllinux_1_2_x86_64.whl", hash = "sha256:7ae7375f803b5520dc9f546bed7e3a0acb70b91812e9bb4b19927de22f25b77d", size = 10741702, upload-time = "2026-10-01T18:03:10.775Z" },
    { url = "https://files.pythonhosted.org/packages/78/fa/0f9c2020dc316c53d983be011720b8157cc052b97e3f4dfa7db6d0f880a6/ruff-0.16.10-py3-none-win32.whl", hash = "sha256:2a12e01cb9156c10c466f63b46eaae5ecea28dfbd21b5836353ae498e7d1349a", size = 10139176, upload-time = "2026-10-01T18:03:13.267Z" },
    { url = "https://files.pythonhosted.org/packages/99/29/cfb0df9448d4d4ad48c2de029ada9ebd71baa6da983a6c77ee6c6cd0fe82/ruff-0.16.10-py3-none-win_amd64.whl", hash = "sha256:97f2015c92aa97105b0eab19eb5d224884399281cfc5da86a92db4ab5e7fb2ca", size = 10584734, upload-time = "2026-10-01T18:03:16.006Z" },
    { url = "https://files.pythonhosted.org/packages/fc/05/c16957eb287c3fc062e032619a25868d93d408a844b725bcf514f7a378ff/ruff-0.16.10-py3-none-win_arm64.whl", hash = "sha256:25a65fe998c4e6861ec079ada5826a2fc605e6cbccbe9dcd7fac1f54e791621b", size = 10366440, upload-time = "2026-10-01T18:03:19.04Z" },
]

[[package]]
name = "ty"
version = "0.0.85"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/66/8f/8de9c4ff90e7131a3c832ea074e123d551fed84c899d37a522f649ca7c6a/ty-0.0.85.tar.gz", hash = "sha256:ef442cbc2fd6dad02eb00dee4213c1e0f18e09bcbeec2cdce6aa802603c5c6bb", size = 7519853, upload-time = "2026-10-06T22:05:41.732Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/1f/06/1716c1778088c5c8f96b248f0e0304e839ca69c096bde82b827bc00e4194/ty-0.0.85-py3-none-linux_armv6l.whl", hash = "sha256:012d71e0dcb51e74599adfb0e5c1416bdac3bf983115e42230545c782b06cfca", size = 14097338, upload-time = "2026-10-06T22:04:58.838Z" },
    { url = "https://files.pythonhosted.org/packages/4a/26/d6b2c7221096c3fa36a0afd4aa8134ffd450df63635ec3862a5a8cf6c9fd/ty-0.0.85-py3-none-macosx_10_12_x86_64.whl", hash = "sha256:391d1993ea3b26509ddb3878dbe79e4cb92487c73109893ee2e51394846e0a69", size = 13684794, upload-time = "2026-10-06T22:05:02.204Z" },
    { url = "https://files.pythonhosted.org/packages/e7/7a/dd1e2e1c54551d61451c18eeb918db833fdbc0a48022fd2bffc93c755735/ty-0.0.85-py3-none-macosx_11_0_arm64.whl", hash = "sha256:90e1bb090348cb560c7ba6109f2c898735b0520fd3114cd316d8bd80439aabb7", size = 13318789, upload-time = "2026-10-06T22:05:04.61Z" },
    { url = "https://files.pythonhosted.org/packages/ff/9c/6c4fc7badf3e1e2e160d0b5c68632d85eb48dd0341422ac44fdd855d1eaf/ty-0.0.85-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:311c131f735bf76be8852305817d5fd10165d6289c76350f6188b0749a66a7f8", size = 13526827, upload-time = "2026-10-06T22:05:07.046Z" },
    { url = "https://files.pythonhosted.org/packages/ba/e5/f6f2d279ef810d89b688425a72150bbbd84a2d6bf54eb9a5ae172f13e3a5/ty-0.0.85-py3-none-manylinux_2_17_armv7l.manylinux2014_armv7l.whl", hash = "sha256:a0971dc7b2f9e9cabdf654f53c8a40e563921227d05567b670f171cba2b3e385", size = 13823871, upload-time = "2026-10-06T22:05:09.731Z" },
    { url = "https://files.pythonhosted.org/packages/47/5d/1210c1f59e8c8c970807a2f13c180fa953ce58a6ddf28e90564db6f8890d/ty-0.0.85-py3-none-manylinux_2_17_i686.manylinux2014_i686.whl", hash = "sha256:5fada6d10172b4c88d44b1f9697c9f5f40d34f8fb40fe716da0366f094268c9b", size = 14727151, upload-time = "2026-10-06T22:05:12.299Z" },
    { url = "https://files.pythonhosted.org/packages/20/26/cdd96e45c33079174d5cd70649a5ae77758bc209f0685e8a4fecee9b7094/ty-0.0.85-py3-none-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl", hash = "sha256:d06c9aa616672e9f9856ff7b539be5c3a4719702e5636e58b4196a8c850a884b", size = 15148511, upload-time = "2026-10-06T22:05:15.304Z" },
    { url = "https://files.pythonhosted.org/packages/f0/28/fd471f2edc0f38a70f0494f9949d1983591073555d254031542c0ed29454/ty-0.0.85-py3-none-manylinux_2_17_s390x.manylinux2014_s390x.whl", hash = "sha256:2280d31c369ef61ed9a4c2399cd663340d85a5fd7965a8ad881203ea6b8b130e", size = 15090530, upload-time = "2026-10-06T22:05:17.874Z" },
    { url = "https://files.pythonhosted.org/packages/7b/4f/6ebfe4f14c399856fc80c448ab442521072f688dfde72b075d8a90d7cafa/ty-0.0.85-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:cc1fff0eab4e73fcc66df761a7a4759da04d3e9c2b82d57c628c50434e2ff0d7", size = 14322051, upload-time = "2026-10-06T22:05:20.366Z" },
    { url = "https://files.pythonhosted.org/packages/36/38/866054d20e12e72a76a37eaf60f1374f7ad4d0b973c145685782065d84cf/ty-0.0.85-py3-none-manylinux_2_31_riscv64.whl", hash = "sha256:453dcb85b5f2486ddc6ade57a50698e9a8d8e3aae34e50f0b20bc5e8c2a3bc2b", size = 14637631, upload-time = "2026-10-06T22:05:22.628Z" },
    { url = "https://files.pythonhosted.org/packages/08/16/700c730b4978de81bab82974c23db0229e58d852e10767e1f1f8b0e217db/ty-0.0.85-py3-none-musllinux_1_2_aarch64.whl", hash = "sha256:820eb594b1d30cd6a0776e59449ed6994b03c27af8da0c287ad351de193eb4a7", size = 13553358, upload-time = "2026-10-06T22:05:24.903Z" },
    { url = "https://files.pythonhosted.org/packages/2e/60/d2dda3a3443d55083429b1eccabed95cbf8769bc61c51831e0ece890780f/ty-0.0.85-py3-none-musllinux_1_2_armv7l.whl", hash = "sha256:4b76c6a2fc5974fc2c5f95156a34f44127be794f4b3dc9793aae5b6a4b774e83", size = 13837412, upload-time = "2026-10-06T22:05:27.163Z" },
    { url = "https://files.pythonhosted.org/packages/f2/54/05043adf78fa5c0440fe9b956505b24d2568da256b60e7479c691510bb92/ty-0.0.85-py3-none-musllinux_1_2_i686.whl", hash = "sha256:0e3a32de0731efce574367fdd680b7524c681909a92e6cf64bb40ad48ccbc110", size = 14167568, upload-time = "2026-10-06T22:05:29.519Z" },
    { url = "https://files.pythonhosted.org/packages/9d/31/0372621051cc807f23d2e9c55bab65818ed131852c05fbe4c65be365895e/ty-0.0.85-py3-none-musllinux_1_2_x86_64.whl", hash = "sha256:d622348c05a9fe99ad087dc93f174617a96f9fef23dd7a0acbdb0adaf8bd5ae6", size = 14489824, upload-time = "2026-10-06T22:05:32.089Z" },
    { url = "https://files.pythonhosted.org/packages/b5/64/0fca31db8c48dc72285f17b878e2c6a015279ab04a26e16f62abb384094f/ty-0.0.85-py3-none-win32.whl", hash = "sha256:0742d21a002481af8d2324b16ce5df210b5bb7673b0ea1096cfc02745c6b7280", size = 13410281, upload-time = "2026-10-06T22:05:34.418Z" },
    { url = "https://files.pythonhosted.org/packages/f6/a8/65d865185ecb18ee45b85cd99b34aedb3d8a4a9fe0438dab695e1390dbb7/ty-0.0.85-py3-none-win_amd64.whl", hash = "sha256:2636f8255b97c357dac1f9f50ca58f58a49642c8adb5c76643f483401a577014", size = 14112013, upload-time = "2026-10-06T22:05:36.946Z" },
    { url = "https://files.pythonhosted.org/packages/24/40/110b4f01af47fbb061f03e2f8e85cb30dd3d9ea614b2059dfaa058a044a5/ty-0.0.85-py3-none-win_arm64.whl", hash = "sha256:953574167a79d9dba7781238879955fa37fea405393710bfe53069ac82dff4d9", size = 13825189, upload-time = "2026-10-06T22:05:39.467Z" },
]

[[package]]
name = "typing-extensions"
version = "4.16.0"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/f6/cc/6253133b5bb138fc3306cebfbda2c520f545d36b5be2c7255cc528bb45d6/typing_extensions-4.16.0.tar.gz", hash = "sha256:dc983d19a509c94dba722ee6abd33940f7c05a89e243c47e907eb4db6f1a43e5", size = 113555, upload-time = "2026-07-02T08:40:05.92Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/49/d3/b8441a820a491ddfc024b0b0cf0393375b75ea13866d9c66727e54c2fc80/typing_extensions-4.16.0-py3-none-any.whl", hash = "sha256:481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8", size = 45571, upload-time = "2026-07-02T08:40:04.659Z" },
]

[[package]]
name = "watchfiles"
version = "1.3.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "anyio" },
]
sdist = { url = "https://files.pythonhosted.org/packages/b3/68/e6aa0b77d217b31f8f486ec0cdfe5e00e6e38dc0be657e7d85819b9faf0a/watchfiles-1.3.0.tar.gz", hash = "sha256:99aee4a07847c06820765fd7b1b49ceac4f3f711ccb7d104655a33231de1c207", size = 108119, upload-time = "2026-09-21T09:08:55.664Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/68/fa/c0b840d5d8bafe640925408ce11095948c8945bb61be1e67d0ab629b872a/watchfiles-1.3.0-cp310-abi3-macosx_10_12_x86_64.whl", hash = "sha256:000b9688fc8133037a8b075c8ebf98f32844ff8964dda61e85c1db547dafc441", size = 399703, upload-time = "2026-09-21T09:08:13.518Z" },
    { url = "https://files.pythonhosted.org/packages/c7/8a/894799b485fe9473ad10422a0d9668e53fb78e3a2b5cc6061159572844ad/watchfiles-1.3.0-cp310-abi3-macosx_11_0_arm64.whl", hash = "sha256:bbc1198edfdc90fda0600f825aa94150f428dfcbf8138746f55998e0e660d64c", size = 397647, upload-time = "2026-09-21T09:08:15.16Z" },
    { url = "https://files.pythonhosted.org/packages/5a/61/f277cd5ead05f5d37b98b41fbdd0c943ee0c04d49738f62e902cb291cf43/watchfiles-1.3.0-cp310-abi3-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:4af9c464d410e8c44b58ddf1cbec7c3a02c1cb2c6c80df9c74659ba2fbda0ab5", size = 454994, upload-time = "2026-09-21T09:08:16.587Z" },
    { url = "https://files.pythonhosted.org/packages/46/66/ea4c01382975e53b1ac1b0a0ea1b353416b8127fb6e04f5c1c313119aab6/watchfiles-1.3.0-cp310-abi3-manylinux_2_17_armv7l.manylinux2014_armv7l.whl", hash = "sha256:eb94e40b9a0db19636b5e3fed0a9803452ecc7381df13b385272abb779ee83ca", size = 460105, upload-time = "2026-09-21T09:08:17.961Z" },
    { url = "https://files.pythonhosted.org/packages/31/c3/1a501b597817096c9831c255f6270c124ce0e2faeb74124be24dcc93b86d/watchfiles-1.3.0-cp310-abi3-manylinux_2_17_i686.manylinux2014_i686.whl", hash = "sha256:7398930a2b76b9dc67a4e6b8bfc7baf30946892a86f417a3920c07bdd6febc30", size = 493761, upload-time = "2026-09-21T09:08:19.327Z" },
    { url = "https://files.pythonhosted.org/packages/5a/16/77352d05e152c7786a016e9f1decdb4507e8aa5bcf3343c72142a0413d14/watchfiles-1.3.0-cp310-abi3-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl", hash = "sha256:025b108f2d5cc2799cb941f79380df3e8b22bfb589c218e801767fe78d598c95", size = 577500, upload-time = "2026-09-21T09:08:20.723Z" },
    { url = "https://files.pythonhosted.org/packages/95/fe/81001c55b24466fe9911135e50269fd3a29f43e446627a92adfab54553b6/watchfiles-1.3.0-cp310-abi3-manylinux_2_17_s390x.manylinux2014_s390x.whl", hash = "sha256:be9ef3cd403d756a304a0a08a112163c63da7ec72c8c9d083c98818291ff8f29", size = 469209, upload-time = "2026-09-21T09:08:22.346Z" },
    { url = "https://files.pythonhosted.org/packages/8a/cf/e3ad894ed5909a7c44b0707e89bc25d19a3d78b3a7aec846119443b6ae56/watchfiles-1.3.0-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:b5768b49e426fd5b550b012c866db347cdf15c398ef98dc557b6e6b72fa74cd1", size = 458353, upload-time = "2026-09-21T09:08:23.7Z" },
    { url = "https://files.pythonhosted.org/packages/7f/f5/2f106829e6e2bc91ad74614730f6df484202b9a4d20d927dbf2f08d37d44/watchfiles-1.3.0-cp310-abi3-manylinux_2_31_riscv64.whl", hash = "sha256:d36c72fcdc08f143d87316a4c4c3b064e340da2c7383d39803950740ed418935", size = 468707, upload-time = "2026-09-21T09:08:25.167Z" },
    { url = "https://files.pythonhosted.org/packages/15/37/2741ab776b978669c1f3bba1e573f1a184f727ab8b4d3a6d9c61090800ed/watchfiles-1.3.0-cp310-abi3-musllinux_1_1_aarch64.whl", hash = "sha256:f0c9865240e065a2247f4b5248528ae3d01e0e8ae071462c250c884dc16e3ee3", size = 632510, upload-time = "2026-09-21T09:08:26.532Z" },
    { url = "https://files.pythonhosted.org/packages/48/64/db4a4684275fe9b696ee5118c194705c1423b3d42181c3f8ee70194d5c73/watchfiles-1.3.0-cp310-abi3-musllinux_1_1_x86_64.whl", hash = "sha256:380f513d26cc2e598266b88d66456e07d67ef4be8f0f435a1154d9c44b43d509", size = 661723, upload-time = "2026-09-21T09:08:28.004Z" },
    { url = "https://files.pythonhosted.org/packages/52/80/95ddb24f6a2f595c031c24432ab7b8aa7d6d1ada0c6d63a552166e06e8d1/watchfiles-1.3.0-cp310-abi3-win32.whl", hash = "sha256:509d9f74d2bec5c1f4cd868ddcfe0c9601f7ea53066dfcb19d8ede742c4de661", size = 277761, upload-time = "2026-09-21T09:08:29.335Z" },
    { url = "https://files.pythonhosted.org/packages/48/a1/1c4a1b3c8030cd03206232612be8a6e8799093490c220b0fcb935d02b75a/watchfiles-1.3.0-cp310-abi3-win_amd64.whl", hash = "sha256:1acabde19b67e673274e89a04d613b7fb1f122e2c4b8ec9a581e59c149264b61", size = 290643, upload-time = "2026-09-21T09:08:30.45Z" },
    { url = "https://files.pythonhosted.org/packages/82/e0/d2db577c632d26d08078c4390dd870b8555c4e558df25d22270f0166c71f/watchfiles-1.3.0-cp310-abi3-win_arm64.whl", hash = "sha256:d978cc1dd7ba44f5590d7de74f7a9c8be7262d9e469c2c0efb8bbfc2574321dc", size = 285510, upload-time = "2026-09-21T09:08:31.561Z" },
    { url = "https://files.pythonhosted.org/packages/4f/55/a122743607939429ab6a7272672f49303aa02bbd34c3f06676765a3861de/watchfiles-1.3.0-cp314-cp314t-macosx_10_12_x86_64.whl", hash = "sha256:e0204f90677b7fb8d3a824279a71a01166bea9f6e53923b8056592d87b33b0b6", size = 395978, upload-time = "2026-09-21T09:08:32.747Z" },
    { url = "https://files.pythonhosted.org/packages/3e/9d/0ee1b0ea42acfe72afa2484f0222e2386dd09992e9034a81e63cc3cdab0a/watchfiles-1.3.0-cp314-cp314t-macosx_11_0_arm64.whl", hash = "sha256:7c1125e99f84934a92996ae343501285617373acd66f16b59fd5654b27ad8d80", size = 387997, upload-time = "2026-09-21T09:08:33.953Z" },
    { url = "https://files.pythonhosted.org/packages/b7/f2/4319c6b683e8bd28465dfc53c750617a2a07f072eb2e3ab0182ccf812229/watchfiles-1.3.0-cp314-cp314t-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:a85e243c87109d9f48a2e0d10d6abdee8768cc114848b32281ec83d7f81d86ef", size = 448067, upload-time = "2026-09-21T09:08:35.104Z" },
    { url = "https://files.pythonhosted.org/packages/b7/71/9f37ac192a51a24de3a2d7fe9aac1e99b2b2668300674ff7a9f85d95beb1/watchfiles-1.3.0-cp314-cp314t-manylinux_2_17_armv7l.manylinux2014_armv7l.whl", hash = "sha256:dd538c71766c59c732e2c5cedc39323c99c11897b99f93eac773438e54af206a", size = 452881, upload-time = "2026-09-21T09:08:36.238Z" },
    { url = "https://files.pythonhosted.org/packages/34/07/1224667c32a4a96876ddd642da69733cbfe6a15897db0865aec5a882cebc/watchfiles-1.3.0-cp314-cp314t-manylinux_2_17_i686.manylinux2014_i686.whl", hash = "sha256:da213822ec9082b62cadf3008e07a8c690ec7a3c89f6dc5e55a8cf07b56a1b26", size = 484802, upload-time = "2026-09-21T09:08:37.717Z" },
    { url = "https://files.pythonhosted.org/packages/bd/4d/7f29cd87e1f826df86fc0418d0b8f370ca0311c29c618406dc492aad9951/watchfiles-1.3.0-cp314-cp314t-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl", hash = "sha256:d4593392e87669836670f87d62fc754059eaeb0e6157af44060a46558cebe5a3", size = 567522, upload-time = "2026-09-21T09:08:38.94Z" },
    { url = "https://files.pythonhosted.org/packages/e3/ac/3aa1f84abd4dbbfbae99a817dd931f77b439261c911189cad4c30fdfd470/watchfiles-1.3.0-cp314-cp314t-manylinux_2_17_s390x.manylinux2014_s390x.whl", hash = "sha256:26b81bc515a0f03f66a69a6fea86eea54c8eca4173c46dd7222569f79dd2f977", size = 461997, upload-time = "2026-09-21T09:08:40.142Z" },
    { url = "https://files.pythonhosted.org/packages/82/1c/27c66764d5b0dbb70a36770a32eca217eba739c28b24e8583a035087a3d7/watchfiles-1.3.0-cp314-cp314t-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:ca39661934749df580d89f3dde266f2af7c6968f4c21c72ce2dc387d299e6aa7", size = 451856, upload-time = "2026-09-21T09:08:41.305Z" },
    { url = "https://files.pythonhosted.org/packages/1e/b3/a45827084d953c1d0dd3d75abf85dcac26a0f5d115ad2fe0b7e9e931573b/watchfiles-1.3.0-cp314-cp314t-manylinux_2_31_riscv64.whl", hash = "sha256:04c5500faa725d69a99b0f63750e80795e455bb951849e9c98a811b4324997c4", size = 459889, upload-time = "2026-09-21T09:08:42.58Z" },
    { url = "https://files.pythonhosted.org/packages/7a/3d/07740d23ce2bb23419bb24055c435a9abe5fe03efdaea1ba0720b831aab6/watchfiles-1.3.0-cp314-cp314t-musllinux_1_1_aarch64.whl", hash = "sha256:ec3cd4bb181a7b6329134204c2277c7144ab5f62cce9c5335d6f901ee7ce8d6a", size = 624482, upload-time = "2026-09-21T09:08:44.064Z" },
    { url = "https://files.pythonhosted.org/packages/91/46/9540f8123eaec86df989f26d7704cad0448d9fb7271763a4f8f9fe23617d/watchfiles-1.3.0-cp314-cp314t-musllinux_1_1_x86_64.whl", hash = "sha256:e5871d4a7f788a9f64fb06f5793389d29d171e5c32d37c3ebfd520b017cc7694", size = 653724, upload-time = "2026-09-21T09:08:45.257Z" },
    { url = "https://files.pythonhosted.org/packages/25/9d/b9deb52f1e4528ffe44338c5ebab95c32ed79203082da661de50288e130a/watchfiles-1.3.0-cp314-cp314t-win32.whl", hash = "sha256:81c989d7267bfb7b676cd32c83bec97914e396870983cbf493e29415037bff5e", size = 270863, upload-time = "2026-09-21T09:08:46.518Z" },
    { url = "https://files.pythonhosted.org/packages/59/59/8b1881afccbafda06248be4185e28034dd73c80c85e4da24f2cb0c1321eb/watchfiles-1.3.0-cp314-cp314t-win_amd64.whl", hash = "sha256:d754e049006e81a9be49dc78ba7802081cee426e968cbc63ee19e164fa2d0e39", size = 286879, upload-time = "2026-09-21T09:08:47.874Z" },
    { url = "https://files.pythonhosted.org/packages/46/dd/41c12ae9745d5d72f709333287679d71cbba68ad7678fed872207bba94f4/watchfiles-1.3.0-cp314-cp314t-win_arm64.whl", hash = "sha256:a5b631db08fd3032db57ec6a92d1777cd60f88803287e4e941a4858c53aab1e0", size = 276924, upload-time = "2026-09-21T09:08:48.976Z" },
]



================================================
FILE: docs/audit-logs.md
================================================
# Audit Log

awesome-python is audited section by section. Every entry gets re-verified against live data, and every removal lands in a commit whose body carries the reason. Git history is the archive. This file is the at-a-glance register of maintainer decisions that a single commit can't show.

## Overrides

[CONTRIBUTING.md](../CONTRIBUTING.md) allows the maintainer to exceed any limit for a specific entry or use case. Each override is recorded here.

### Naming Exceptions

Display names follow the canonical PyPI package name. These entries keep a different name by maintainer decision:

- autobahn-python -- `autobahn`.
- django-rest-framework -- `djangorestframework`.
- django-rules -- `rules`.
- fasthtml -- `python-fasthtml`.
- graphify -- `graphifyy`.
- jinja -- `Jinja2`.
- mem0 -- `mem0ai`.
- pangu.py -- `pangu`.
- playwright-python -- `playwright`.
- pytorch -- `torch`.
- strawberry -- `strawberry-graphql`.
- strawberry-django -- `strawberry-graphql-django`.
- thealgorithms -- not on PyPI; its GitHub repo name is `Python`.

### Stability Exceptions

Entries admitted despite the Stable quality requirement, by maintainer decision:

- zensical -- admitted 2026-08-23 at version 0.0.57, PyPI classifier `Development Status :: 3 - Alpha`, with no 1.0 target announced. Admitted as a challenger displacing mkdocs because the Documentation section was carrying a dying upstream: the Material for MkDocs team's announcement of 2025-11-05 put Material into maintenance mode for twelve months and called MkDocs itself unmaintained since 2024-08 and a supply chain risk. Re-check when 1.0 lands.
- openviking -- admitted 2026-08-25 (PR #3302) at version 0.4.16, PyPI classifier `Development Status :: 3 - Alpha`, with a README that said "OpenViking is still in its early stages". Admitted as a Data Layer challenger because the adoption is real: 459,446 downloads/month on pypistats (mirror-excluded) on 2026-08-24, and releases every few days. Re-check when 1.0 lands.
- claude-agent-sdk -- kept 2026-10-01 in the AI and Agents audit at version 0.2.163, PyPI classifier `Development Status :: 3 - Alpha`. Kept as a Vendor Agent SDKs obvious choice because the adoption is real: 30,033,689 downloads/month on ClickPy on 2026-10-01, up from 1.2M in March 2026 on pypistats. Re-check when 1.0 lands.
- uv-audit -- kept 2026-08-16 as a Supply Chain Security entry, recorded 2026-10-02. uv itself prints "`uv audit` is experimental and may change without warning". Kept because it is part of uv, the obvious package manager. Re-check when uv drops the experimental notice.

### Challenger Exceptions

Entries admitted as challengers without adoption-trajectory evidence, by maintainer decision:

- seleniumbase -- admitted 2026-08-16 (PR #3284) as a Browser Automation challenger. It wraps selenium, the successor trajectory in the use case belongs to playwright, and its distinct value is its stealth/UC mode. Admitted because that stealth value counts toward Browser Automation.
- semantica -- kept 2026-10-01 in the AI and Agents audit as a Data Layer challenger at 16,582 downloads/month on ClickPy, with no adoption-trajectory evidence found. Kept by maintainer decision.
- hyperopt -- admitted 2026-10-16 as a Hyperparameter Optimization challenger at 1,793,872 downloads/month on ClickPy. Its 0.3.0 release came after a 4.5-year gap and it has no adoption-trajectory evidence. Admitted by maintainer decision.
- magika -- admitted 2026-10-16 as a File Type Detection challenger at 16,388,380 downloads/month on ClickPy. markitdown requires it, so most of that count is transitive, and no adoption-trajectory evidence was found. Admitted by maintainer decision.

### Cap Exceptions

Use cases holding more than 5 entries, by maintainer decision:

- Asynchronous Programming > Async I/O -- 6 entries since the 2026-08-16 split (19875cf), recorded 2026-10-02.
- Code Analysis > Linters and Formatters -- 6 entries since Security Linters merged in on 2026-08-16 (3290ce5), recorded 2026-10-02.
- Package Management > Package Managers -- 6 entries since the subcategory was minted on 2026-08-16 (1b51907), recorded 2026-10-02.

### Mature-stable Keeps

These entries sit past the 12-month activity requirement without an override. Each one is kept by editorial judgment: mature, stable, and no successor exists.

- annoy -- kept 2026-10-02 in the AI & ML audit, last push 2025-10-29. Unlike the others it has a successor, Spotify's own Voyager (2023), but kept by maintainer decision on 911,913 downloads/month on pypistats.
- blinker -- recorded 2026-10-02 ahead of its activity-line crossing on 2026-11-19 (last push 2025-11-19, last release 1.9.0 on 2024-11-08). Flask requires it.
- diskcache -- kept 2026-10-02, last push 2024-08-10, last release 5.6.3 (2023-08-31). Kept despite an unpatched pickle deserialization advisory, CVE-2025-69872 (GHSA-w8v5-vhqr-4h9v), on 25,526,045 downloads/month on ClickPy.
- django-rules -- recorded 2026-10-02 ahead of its activity-line crossing on 2026-10-11 (last push 2025-10-11, last release 3.5 on 2024-09-02).
- ftfy
- gensim -- recorded 2026-10-15 ahead of its activity-line crossing on 2026-11-01 (last push 2025-11-01, last release 4.4.0 on 2025-10-18), on 2,904,015 downloads/month on ClickPy (2026-10-12).
- httpie -- kept 2026-08-16, recorded 2026-10-02. Last commit 2024-12-17, last release 3.2.4 on 2024-11-01.
- itsdangerous
- jieba
- jinja
- python-pptx -- kept 2026-10-02, last commit 2024-08-06, last release 1.0.2 on 2024-08-07. No successor for generating .pptx files.
- schedule -- kept 2026-08-16, recorded 2026-10-02. Last commit 2024-05-25.
- sortedcontainers

## Rejected Additions

Projects the maintainer decided not to list, with the evidence at decision time, keyed by GitHub `owner/repo` (`owner/*` for a whole organization). PR reviews and star scans check here before proposing a project again. Rejudge one only on new evidence.

- BrianPugh/autoregistry -- 2026-08-23, 16,758 downloads/month: 77 stars.
- MarcBresson/schedium -- 2026-08-23, 381 downloads/month: repository created 2026-02-05.
- ets-labs/python-dependency-injector -- 2026-08-23, 9,086,069 downloads/month: the Dependency Injection use case was declined, since FastAPI's Depends and pytest fixtures absorb most of the need, leaving a leader with no challenger field.
- konradhalas/dacite -- 2026-08-23, 23,147,569 downloads/month: last push 2025-03-17, fails the activity rule.
- reagento/dishka -- 2026-08-23, 769,893 downloads/month: declined with the Dependency Injection use case.
- xberg-io/* -- 2026-08-16: coordinated multi-entry self-promotion; four planted entries were removed (xberg, liter-llm, tree-sitter-language-pack, html-to-markdown). Reject any project from this organization on sight.
- AbstractUmbra/audioop -- 2026-10-16, 7,714,737 downloads/month (ClickPy): gradio and discord.py require it on Python 3.13+, so the count is transitive. It is a backport of a removed stdlib module, not an audio tool readers choose.
- alteryx/featuretools -- 2026-10-16, 106,521 downloads/month (ClickPy): Fails Active: last commit 2024-11-13, last release 2024-05-14.
- AnswerDotAI/fastcore -- 2026-10-16, 24,139,424 downloads/month (ClickPy): ghapi requires it, and the jump from 11.5M to 50.9M is pull from that dependency. It is a fastai grab-bag, not a built-in class enhancement.
- anthropics/claude-code-security-review -- 2026-10-16, no PyPI download signal: A language-agnostic GitHub Action with no releases and no commits since 2026-02-11. Not Python work.
- apple-aiml-research/ml-stable-diffusion -- 2026-10-16, no PyPI download signal: Fails Active: the last human commit is 2025-07-03, and the 2026 commit is a bot. It is a Core ML/Swift path, not a Python generation library.
- arrobalytics/django-ledger -- 2026-10-16, 17,102 downloads/month (ClickPy): An accounting engine, not an ERP suite. Small demand, no Development Status classifier, and no production case studies found.
- asdf-vm/asdf -- 2026-10-16, no PyPI download signal: The tool users are leaving for mise, with the 0.16 Go rewrite cited as the trigger. PyPI "asdf" is an unrelated astronomy package.
- AUTOMATIC1111/stable-diffusion-webui -- 2026-10-16, no PyPI download signal: Fails Active: the last commit on the default branch is 2024-07-27, and its pushed_at date doesn't reflect code changes.
- binaryornot/binaryornot -- 2026-10-16, 13,794,027 downloads/month (ClickPy): cookiecutter requires it, which accounts for about half the count. It does a narrow job, and the use case is at cap.
- bisohns/search-engine-parser -- 2026-10-16, 22,138 downloads/month (ClickPy): Last release 2022-11, and it pins lxml<5. It scrapes search results pages, not page content.
- bookieio/breadability -- 2026-10-16, 106,712 downloads/month (ClickPy): sumy pulls in almost all of the count. Its first release since 2014 lists Python 3.6 classifiers.
- boson-ai/higgs-audio -- 2026-10-16, 416 downloads/month (ClickPy): Two releases, both on 2025-10-03, and the PyPI homepage is a placeholder. v3 moved to Hugging Face plus an API, so nothing pip-installable is maintained.
- caesar0301/treelib -- 2026-10-16, 1,532,895 downloads/month (ClickPy): anytree (6.0M) is the bigger tree library at 4x the downloads, so treelib is not the obvious choice.
- chibisov/drf-extensions -- 2026-10-16, 2,067,903 downloads/month (ClickPy): Last release declares Django<6.0, and it is a DRF add-on, not an API framework.
- cknd/stackprinter -- 2026-10-16, 334,597 downloads/month (ClickPy): Flat downloads, and one release after a two-year gap. No sign of a challenger trajectory.
- clips/pattern -- 2026-10-16, no PyPI download signal: The code ended in 2018, and the 2026 commit is a README edit. PyPI "pattern" is now an unrelated package. Previously removed 2026-03-21 (f52c85a) as unmaintained, and nothing has changed since.
- closeio/ciso8601 -- 2026-10-16, 6,373,074 downloads/month (ClickPy): The use case is full. Its own docs tell users on Python 3.11+ to use datetime.fromisoformat unless they need the speed, so it is a narrow speed-up, not a general datetime library.
- codelucas/newspaper -- 2026-10-16, 468,795 downloads/month (ClickPy): The 2026-03-21 removal (1d09426, unmaintained) still holds: last release was 2018-09, and the 2026 push came with no release.
- coleifer/unqlite-python -- 2026-10-16, 11,386 downloads/month (ClickPy): It binds an embedded database rather than being a server driver, and has negligible demand in either home.
- coleifer/walrus -- 2026-10-16, 182,584 downloads/month (ClickPy): A utility layer over redis-py, not a driver, at under 0.1% of redis's 204M downloads.
- crccheck/django-object-actions -- 2026-10-16, 2,366,676 downloads/month (ClickPy): An add-on for Django admin buttons, not an admin panel. The source of its download count is unknown.
- davidhalter/jedi -- 2026-10-16, 102,370,894 downloads/month (ClickPy): ipython requires it, and its count almost exactly matches ipython's 102.6M. Its job is editor and REPL autocompletion, which the list dropped along with the Editor Plugins section (c87fdac).
- DerwenAI/pytextrank -- 2026-10-16, 82,707 downloads/month (ClickPy): Fails Active: last commit 2024-05-21, last release 2024-02-21.
- django-haystack/celery-haystack -- 2026-10-16, 1,919 downloads/month (ClickPy): Last release 2015-12.
- django-parler/django-parler -- 2026-10-16, 160,493 downloads/month (ClickPy): django-modeltranslation (826,853) has 5x its downloads, so it is not the obvious choice for Django model translation.
- doableware/djongo -- 2026-10-16, 57,392 downloads/month (ClickPy): Its latest release (1.3.7, 2024-11) pins django<=3.1.12, so it can't be installed with any supported Django. django-mongodb-backend already does this job.
- Doist/bitmapist -- 2026-10-16, 7,385 downloads/month (ClickPy): A Redis bitmap analytics library, not a driver, with negligible demand. Its metadata caps Python below 3.14 and redis below 6.0.
- dpath-maintainers/dpath-python -- 2026-10-16, 8,884,938 downloads/month (ClickPy): checkov and airbyte-cdk pull it in, leaving about 3.5M independent, below the section's floor (python-box, 4.9M). Last release 2024-06.
- dpkp/kafka-python -- 2026-10-16, 17,148,353 downloads/month (ClickPy): It was removed as unmaintained on 2026-03-21 (e8d3d29), but it was still releasing then and has shipped 3.0.0 through 3.0.11 since (June to August 2026), so that reason no longer holds. It is held back by tier: confluent-kafka (41.5M) is the default for new projects, and kafka-python is the pure-Python fallback rather than a successor.
- dwolfhub/zxcvbn-python -- 2026-10-16, 4,673,093 downloads/month (ClickPy): Password-strength estimation is not cryptography, and there is no use case for passwords. It also fails Active: last commit on master was 2025-10-06.
- explorerhq/sql-explorer -- 2026-10-16, 213,897 downloads/month (ClickPy): A SQL reporting tool, not an admin panel, and below the smallest incumbent (django-grappelli, 281,247).
- frostming/marko -- 2026-10-16, 5,798,780 downloads/month (ClickPy): The obvious tier (markdown-it-py, markdown, mistune) is full. Its growth roughly tracks the general ClickPy inflation, and no source shows it replacing any of the three.
- ggml-org/whisper.cpp -- 2026-10-16, 734,136 downloads/month (ClickPy): Python uses it through the separate third-party absadiki/pywhispercpp (349 stars). It does faster-whisper's job (12.1M) with no sign of overtaking it. The download count is unexplained for 349 stars.
- gitleaks/gitleaks -- 2026-10-16, no PyPI download signal: Secret Scanning was minted with betterleaks alone. gitleaks is a language-agnostic Go binary with slowing activity (last release 2026-03-21).
- hhatto/autopep8 -- 2026-10-16, 7,132,827 downloads/month (ClickPy): The use case holds 6 entries under a cap exception, and none is weaker (flake8 39.6M, bandit 24.5M). Last release was 2025-01, and the 2026 commits are dependabot only.
- html5lib/html5lib-python -- 2026-10-16, 26,055,801 downloads/month (ClickPy): The 2026-03-21 removal (7f21136, no release since 2019) still holds: last release 1.1 in 2020-06. The count comes from 3,281 dependents rather than people picking it, and justhtml already covers pure-Python HTML5 parsing.
- huggingface/speech-to-speech -- 2026-10-16, 2,714 downloads/month (ClickPy): An end-to-end voice pipeline app, not an ASR/TTS library, and far below the smallest Speech entry (funasr, 297,003).
- jazzband/django-pipeline -- 2026-10-16, 222,640 downloads/month (ClickPy): The 2026-03-21 removal (6b59080) gave overlap with django-compressor as the reason, which still holds: django-compressor has 11x its downloads.
- jundot/omlx -- 2026-10-16, no PyPI download signal: A macOS menu-bar app (repo created 2026-02-13), not a library. mlx-lm already covers Apple Silicon.
- jupyter/docker-stacks -- 2026-10-16, no PyPI download signal: Container images that package notebook (already listed), not an interpreter.
- kaifcodec/user-scanner -- 2026-10-16, 16,772 downloads/month (ClickPy): The use case is at cap. sherlock-project does the same username OSINT job at 4x the downloads. Repo created 2025-10.
- keleshev/schema -- 2026-10-16, 19,658,077 downloads/month (ClickPy): Removed as unmaintained on 2026-03-21 (e8d3d29), and activity has not resumed: the last release was 0.7.8 in 2025-10, with only a push since. It is classified Alpha and is not a successor to pydantic or jsonschema.
- kellyjonbrazil/jc -- 2026-10-16, 626,452 downloads/month (ClickPy): Parser is at cap (floor: parsy, 3.96M). jc does a different job (CLI output to JSON) and has no entry to replace.
- lexiforest/curl_cffi -- 2026-10-16, 31,930,921 downloads/month (ClickPy): About 17.4M of this is pulled in by yfinance, leaving roughly 14M of its own demand. HTTP Clients General is at cap, and web sources frame it as a TLS-fingerprint impersonation tool for getting past anti-bot blocks, not as a successor to requests or httpx2. No use case covers impersonation.
- LPgenerator/django-db-mailer -- 2026-10-16, 1,143 downloads/month (ClickPy): Last release 2018-10.
- mahmoud/glom -- 2026-10-16, 23,112,427 downloads/month (ClickPy): semgrep requires it, leaving about 3.5M independent. It is a transformer for nested data rather than a built-in class enhancement.
- mailgun/flanker -- 2026-10-16, 36,887 downloads/month (ClickPy): The 2026-03-21 removal (7f21136, abandoned by Mailgun) still holds: last release 2019-12. It parses mail rather than sending it.
- matthewwithanm/django-imagekit -- 2026-10-16, 380,436 downloads/month (ClickPy): Django-specific and below General's floor. Django thumbnailing has no clear leader (sorl-thumbnail 485K, easy-thumbnails 469K).
- matthewwithanm/pilkit -- 2026-10-16, 380,588 downloads/month (ClickPy): Pulled in by django-imagekit (nearly identical counts). Last release 2023-09.
- maxfischer2781/asyncstdlib -- 2026-10-16, 4,288,321 downloads/month (ClickPy): Async I/O already holds 6 entries under a cap exception. This is a different job (async versions of builtins and itertools), and aiostream (3.8M) is an equal peer.
- MemPalace/mempalace -- 2026-10-16, 56,453 downloads/month (ClickPy): Data Layer is at cap. Agent memory is mem0's job (2.0M), so there is no one-in-one-out case. Its April 2026 launch coverage centred on disputed benchmarks (the 100% LongMemEval claim was pulled), it is classified Beta, and its popularity is driven by stars (59.6k stars vs 56k downloads).
- mewwts/addict -- 2026-10-16, 6,120,693 downloads/month (ClickPy): Fails Active: last commit 2021-01, last release 2020-11. python-box, already listed, does the same job.
- microsoft/bocpy -- 2026-10-16, 9,933 downloads/month (ClickPy): Created 2026-02, classified Beta, 201 stars. No adoption-trajectory evidence.
- mongodb/motor -- 2026-10-16, 9,226,799 downloads/month (ClickPy): Deprecated in favor of the PyMongo Async API (2025-05-14) and end-of-life since 2026-05-14. Its last release was 3.7.1 in 2025-05, and pymongo is listed. The earlier removal (d9bba73, 2026-01-16, "unmaintained") still holds.
- mpdavis/python-jose -- 2026-10-16, 32,386,854 downloads/month (ClickPy): The 2026-03-21 removal (f50bd8f, superseded) still holds: FastAPI's JWT tutorial now uses PyJWT, and several dependents migrated away after CVE-2024-33663. No release since 2025-05.
- myusuf3/delorean -- 2026-10-16, 107,732 downloads/month (ClickPy): Removed 2024-02-23 (8524f28). 2.0.0 (2026-08) is its first release since 2018, and that day's commits are docs and CI only. It is Beta, has little demand, and the use case is full.
- noripyt/django-cachalot -- 2026-10-16, 244,358 downloads/month (ClickPy): Does the same job as django-cacheops (listed), which has 8x its downloads.
- oobabooga/textgen -- 2026-10-16, no PyPI download signal: A desktop app, not a pip library. PyPI "textgen" is an unrelated package.
- opensanctions/countrynames -- 2026-10-16, 15,360 downloads/month (ClickPy): Narrow job. pycountry (32.2M, unlisted) is the obvious country-data library.
- osantana/prettyconf -- 2026-10-16, 29,957 downloads/month (ClickPy): The use case is full at 5 entries, and prettyconf has about 0.6% of the downloads of dynaconf, the smallest entry.
- pydata/numexpr -- 2026-10-16, 12,883,844 downloads/month (ClickPy): Healthy (2.14.2 released 2026-07), but Core already holds numpy, scipy, and numba with far more demand. numexpr is an older accelerator, not a successor to any of them.
- python-excel/xlrd -- 2026-10-16, 70,465,563 downloads/month (ClickPy): Removed 2026-01-16 (d9bba73) as archived, but the repo was never archived. Releases have not resumed since 2.0.2 (2025-06), its own tagline says to use openpyxl where possible, it reads only legacy .xls, and python-calamine (7.7M) is the recommended replacement. Most of the count is direct demand.
- rajatim/zhtw -- 2026-10-16, 719 downloads/month (ClickPy): 14 stars, created 2025-12. It covers a narrower part of OpenCC's job.
- rushter/MLAlgorithms -- 2026-10-16, no PyPI download signal: Educational code, not on PyPI. thealgorithms already covers this.
- s3tools/s3cmd -- 2026-10-16, 1,243,432 downloads/month (ClickPy): The 2026-03-21 removal (e8d3d29) still holds: last release 2023-12, and it crosses the 12-month activity line on 2026-10-22. awscli and boto3 cover the job.
- saresend/KSUID -- 2026-10-16, 74,743 downloads/month (ClickPy): Fails Active: last commit 2018-11, last release 2017. svix-ksuid (1.0M) is the bigger KSUID library.
- shibing624/text2vec -- 2026-10-16, 2,291 downloads/month (ClickPy): sentence-transformers (listed) covers this, and there is no independent demand.
- smartcrop/smartcrop.py -- 2026-10-16, 29,956 downloads/month (ClickPy): A niche content-aware cropping job at 30K, and General is at cap (floor: pyvips, 867,739).
- SmileyChris/easy-thumbnails -- 2026-10-16, 469,327 downloads/month (ClickPy): Django-specific and below General's floor, with no lead over sorl-thumbnail. Last release 2025-08.
- ssut/py-googletrans -- 2026-10-16, 1,941,718 downloads/month (ClickPy): Fails Active: last commit 2025-04. It is an unofficial Google Translate scraper (machine translation, not i18n).
- TeamHG-Memex/eli5 -- 2026-10-16, 84,428 downloads/month (ClickPy): Fails Active: the maintained fork eli5-org/eli5 last committed on 2025-04-20, and recent commits to the original repo only delete workflow files.
- TheTom/turboquant_plus -- 2026-10-16, no PyPI download signal: A research repo for KV-cache quantization. Every commit since 2026-06-12 is a README edit, and the latest says the work was merged upstream into mlx-swift-lm. Nothing pip-installable.
- thumbor/libthumbor -- 2026-10-16, 66,538 downloads/month (ClickPy): A companion to the listed thumbor. Last release 2022-03, with only dependabot commits since.
- THUwangcy/ReChorus -- 2026-10-16, no PyPI download signal: An academic research framework with 648 stars, not on PyPI.
- tyiannak/pyAudioAnalysis -- 2026-10-16, 13,577 downloads/month (ClickPy): Removed 2026-03-21 (e8d3d29) as unmaintained, and that still holds: last release 2022-02, with only README edits since.
- uploadcare/pillow-simd -- 2026-10-16, 66,174 downloads/month (ClickPy): A fork of the listed pillow with 0.01% of its downloads, and General is at cap.
- wroberts/pytimeparse -- 2026-10-16, 23,637,352 downloads/month (ClickPy): Its count matches agate's (20.8M), which dbt-core pulls in, so very little of it is people choosing pytimeparse. 1.1.9 is its first release since 2018 and is classified Beta. The use case is full.
- x-hw/amazing-qr -- 2026-10-16, 812 downloads/month (ClickPy): Its 10.8k stars don't show up as installs. It pins Pillow<12, while qrcode (28.7M) holds the use case.
- xhtml2pdf/xhtml2pdf -- 2026-10-16, 3,813,456 downloads/month (ClickPy): It was removed in 2016 (a936fd1) as "deprecated in favor of WeasyPrint", which is no longer true: it shipped 0.2.22–0.2.24 in 2026-10. It still fails the tier bar, since the web calls WeasyPrint the default (32.5M) and describes xhtml2pdf as having limited CSS. It is an older alternative, not a successor.
- Yelp/detect-secrets -- 2026-10-16, 9,698,855 downloads/month (ClickPy): Weak maintenance: last release 2024-05, last code commit 2025-01, and only a CI commit in 2026. Demand rose 6.6x with no explained cause.
- youssofal/MTPLX -- 2026-10-16, 7,276 downloads/month (ClickPy): Narrow: its own summary is "Native MTP speculative decoding for Qwen3-Next on Apple Silicon". Repo created 2026-05-02, and it hard-requires mlx-lm, which is already listed, so it is an add-on rather than a separate pick.
- ytdl-org/youtube-dl -- 2026-10-16, 164,180 downloads/month (ClickPy): The 2026-03-21 removal (f50bd8f, replaced by yt-dlp) still holds: no release since 2021.12.17, commits stopped 2025-11, and downloads are falling.

## Last Audited

An audit that changes nothing in a section leaves no commit, so its date is recorded here, one line per section, replaced on each re-audit.

- Asynchronous Programming -- 2026-10-15, no changes.
- Build Tools -- 2026-10-15, no changes.
- CLI Tools -- 2026-10-15, no changes.
- Computer Vision -- 2026-10-15, no changes.
- Configuration Files -- 2026-10-15, no changes.
- Cryptography -- 2026-10-15, no changes.
- Data Analysis -- 2026-10-15, no changes.
- Data Validation -- 2026-10-15, no changes.
- Date and Time -- 2026-10-15, no changes.
- Email -- 2026-10-15, no changes.
- Environment Management -- 2026-10-15, no changes.
- File Manipulation -- 2026-10-15, no changes.
- Functional Programming -- 2026-10-15, no changes.
- Geolocation -- 2026-10-15, no changes.
- HTML Manipulation -- 2026-10-15, no changes.
- Image Processing -- 2026-10-15, no changes.
- Implementations -- 2026-10-15, no changes.
- Interactive Interpreter -- 2026-10-15, no changes.
- Machine Learning -- 2026-10-15, no changes.
- Microsoft Windows -- 2026-10-15, no changes.
- Miscellaneous -- 2026-10-15, no changes.
- Natural Language Processing -- 2026-10-15, no changes.
- Package Management -- 2026-10-15, no changes.
- Quantum Computing -- 2026-10-15, no changes.
- Recommender Systems -- 2026-10-15, no changes.
- Science -- 2026-10-15, no changes.
- Supply Chain Security -- 2026-10-15, no changes.
- Web Security -- 2026-10-15, no changes.



================================================
FILE: docs/adr/0001-shortlist-not-catalog.md
================================================
---
status: accepted
---

# awesome-python is a shortlist of obvious choices, not a catalog

By mid-2026 the list held 576 entries across 75 sections, with entry inflow up 24x year over year (96 additions in the trailing 12 months vs 4 the year before), concentrated in sections like AI and Agents (41 entries). The old acceptance model — three lanes (Industry Standard, Rising Star, Hidden Gem), only the first capped — admitted any project good enough in isolation, so categories grew without bound and stopped answering the reader's actual question: "what do I use for X?" We decided to reposition the list as a curated shortlist, per the Zen of Python: there should be one — and preferably only one — obvious way to do it.

## The decision

The list's scope test is "serves Python developers", replacing the old "primarily written in Python (>50%)" requirement: implementation language and packaging are irrelevant when Python developers use the thing in their Python work (uv and ty are Rust; agent skill packs are markdown), while a pure-Python project nobody uses in Python work does not belong. Each Use Case (a subcategory, or a flat section) lists at most its Obvious Choices — up to 3, plus up to 2 Challengers, hard maximum 5 (numbers provisional, to be reviewed after the prune). Admission is by maintainer editorial judgment, informed primarily by PyPI download counts rather than GitHub stars, and stated as final; judgment overrides the signal's known failure modes (CI/dependency-inflated counts, model releases consumed as weights rather than pip installs, large-but-specific audiences misread as "niche"). Once a Use Case is at cap, the only way in is Displacement: the PR names the entry it replaces and argues the newcomer does that job better. Use Cases are defined by the list's existing structure; an entry PR can never create the subcategory it needs. Standard-library entries hold a slot only where the stdlib module is itself the obvious choice. The existing stock gets the same test retroactively: a staged, worst-first prune (per-section sweep commits), with removed entries deleted outright — git history is the archive. Resources sections (Newsletters, Podcasts, Websites) are out of scope for now.

## Considered options

- Keep the three-lane model with caps on every lane: rejected because the lanes answer the wrong question ("is this good enough to enter?") once admission is comparative; rising-star momentum becomes evidence for a Challenger slot or a Displacement rather than an admission ticket of its own, and Hidden Gem is definitionally incompatible with "obvious".
- Rules-only, no retroactive prune: rejected because every rejection would face "but X is listed" precedent arguments, and readers would see no change.
- Archive removed entries in a separate file: rejected because it recreates the catalog one click away and dilutes the identity the change exists to restore.

## Consequences

- The list shrinks substantially: the maintainer-reviewed preview of the three largest sections kept 45 of 80 entries. Most future PRs will be rejected for fullness, not badness.
- awesome-python.com loses long-tail search traffic for the hundreds of niche tool names it will no longer carry. Accepted deliberately: reader trust over search surface.
- Fast-moving domains (e.g. AI and Agents) list current leaders by usage and absorb churn through Displacement; an oversized Use Case is either trimmed or Split into finer Use Cases by the maintainer.
- Linked awesome-* lists (e.g. awesome-python-testing) remain as the escape valve for readers who want exhaustive catalogs.



================================================
FILE: website/build.py
================================================
#!/usr/bin/env python3
"""Build a single-page HTML site from README.md for the awesome-python website."""

import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from collections import Counter
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import TypedDict
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from jinja2 import Environment, FileSystemLoader
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

from fetch_pypi_downloads_via_clickpy import OVERRIDES_FILE, normalize
from readme_parser import AlsoSee, ParsedGroup, ParsedSection, parse_readme, parse_sponsors, render_inline_text, slugify

GITHUB_REPO_URL_RE = re.compile(r"^https?://github\.com/([^/]+/[^/]+?)(?:\.git)?/?$")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
BULLET_LINE_RE = re.compile(r"^\s*-\s")
ANCHOR_LINK_ATTRS_RE = re.compile(r'href="(#[^"]*)" target="_blank" rel="noopener"')
SITE_URL = "https://awesome-python.com/"
SITEMAP_URL = f"{SITE_URL}sitemap.xml"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
PLURAL_NOUNS = {"Clients", "Drivers", "Engines", "Files", "Frameworks", "Generators", "Implementations", "Panels", "Queues", "Repositories", "Schedulers", "Servers", "Stdlib", "Tools"}

BUILTIN_FILTER = "Stdlib"
BUILTIN_SLUG = "built-in"
BUILTIN_PATH = f"/categories/{BUILTIN_SLUG}/"
BUILTIN_PUBLIC_URL = f"{SITE_URL}categories/{BUILTIN_SLUG}/"

SPONSORSHIP_PATH = "/sponsorship/"
SPONSORSHIP_PUBLIC_URL = f"{SITE_URL}sponsorship/"
SPONSORSHIP_DESCRIPTION = "Sponsorship for Awesome Python: tiers, audience, and how to get your product in front of professional Python developers evaluating tools for production use."

BUNDLED_PREFIX_RE = re.compile(r"^\(part of ")

# Category intros name projects as their docs do, README entries by their PyPI name
PICK_ALIASES = {
    "Airflow": "apache-airflow",
    "Beautiful Soup": "beautifulsoup4",
    "Cacheops": "django-cacheops",
    "Chroma": "chromadb",
    "Coverage.py": "coverage",
    "Django AI Skills": "django-ai-plugins",
    "Django ORM": "django.db.models",
    "Faiss": "faiss-cpu",
    "gRPC": "grpcio",
    "Google Cloud client libraries": "google-cloud-python",
    "Grappelli": "django-grappelli",
    "Hydra": "hydra-core",
    "Ibis": "ibis-framework",
    "Jupyter Notebook": "notebook",
    "Material for MkDocs": "mkdocs-material",
    "MCP Python SDK": "mcp",
    "OpenAI Agents SDK": "openai-agents",
    "OpenCV": "opencv-python",
    "Playwright": "playwright-python",
    "PyAV": "av",
    "Python-Markdown": "markdown",
    "python-oracledb": "oracledb",
    "Ray Core": "ray",
    "redis-py": "redis",
    "Sherlock": "sherlock-project",
    "Silk": "django-silk",
    "Surprise": "scikit-surprise",
    "The Algorithms - Python": "thealgorithms",
    "Unfold": "django-unfold",
    "Vega-Altair": "altair",
}

SOURCE_TYPE_DOMAINS = {
    "docs.python.org": BUILTIN_FILTER,
    "gitlab.com": "GitLab",
    "bitbucket.org": "Bitbucket",
}


class TemplateSubcategory(TypedDict):
    name: str
    value: str
    slug: str
    url: str


class TemplateEntry(TypedDict):
    name: str
    url: str
    description: str
    categories: list[str]
    groups: list[str]
    subcategories: list[TemplateSubcategory]
    stars: int | None
    downloads: int | None
    owner: str | None
    last_commit_at: str | None
    source_type: str | None
    bundled: bool
    badge: str | None
    also_see: list[AlsoSee]


class EntryGroup(TypedDict):
    name: str  # empty for a page with a single unnamed group
    slug: str
    url: str  # links the group heading to its own page, empty when it has none
    lead: str  # the section intro's first paragraph as HTML, shown under the heading on group pages
    entries: list[TemplateEntry]


class SyntheticCategory(TypedDict):
    name: str
    slug: str
    description: str
    description_html: str


TemplateCategory = ParsedSection | SyntheticCategory


def detect_source_type(url: str) -> str | None:
    """Detect source type from URL domain. Returns None for GitHub URLs."""
    if GITHUB_REPO_URL_RE.match(url):
        return None
    for domain, source_type in SOURCE_TYPE_DOMAINS.items():
        if domain in url:
            return source_type
    if "github.com" not in url:
        return "External"
    return None


def extract_github_repo(url: str) -> str | None:
    """Extract owner/repo from a GitHub repo URL. Returns None for non-GitHub URLs."""
    m = GITHUB_REPO_URL_RE.match(url)
    return m.group(1) if m else None


def sponsor_website_url(url: str) -> str:
    """Set utm_content=website so sponsors can tell website clicks from README clicks."""
    parts = urlsplit(url)
    pairs = parse_qsl(parts.query, keep_blank_values=True)
    if not any(k == "utm_content" for k, _ in pairs):
        return url
    query = [(k, "website" if k == "utm_content" else v) for k, v in pairs]
    return urlunsplit(parts._replace(query=urlencode(query)))


def load_stars(path: Path) -> dict[str, dict]:
    """Load star data from JSON. Returns empty dict if file doesn't exist or is corrupt."""
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def load_pypi_badges() -> dict[str, str]:
    """Load the badge each entry shows in place of a download count.

    Keyed by normalized README name. Only entries whose missing count needs
    explaining beyond "Not on PyPI" carry one, e.g. the SDK monorepos that do
    ship on PyPI, just as many per-service packages.
    """
    raw = json.loads(OVERRIDES_FILE.read_text())
    return {name: entry["badge"] for name, entry in raw.items() if entry.get("badge")}


def load_downloads(path: Path) -> dict[str, int]:
    """Load last-30-day download counts from the TSV cache, keyed by normalized README name.

    Columns: name, package, downloads, fetched_at. Skips the header and
    NOT_FOUND rows. Returns empty dict if the file doesn't exist.
    """
    if not path.exists():
        return {}
    downloads: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines()[1:]:
        parts = line.split("\t")
        if len(parts) >= 3 and parts[2].isdigit():
            downloads[parts[0]] = int(parts[2])
    return downloads


def sort_entries(entries: Sequence[TemplateEntry]) -> list[TemplateEntry]:
    """Sort entries by downloads descending, then name ascending.

    Four tiers: entries with download counts first, then starred entries by
    stars descending, then stdlib, then the rest.
    """

    def sort_key(entry: TemplateEntry) -> tuple[int, int, int, str]:
        downloads = entry["downloads"]
        stars = entry["stars"]
        name = entry["name"].lower()
        if downloads is not None:
            return (0, -downloads, 0, name)
        if stars is not None:
            builtin = 1 if entry.get("source_type") == BUILTIN_FILTER else 0
            return (1, -stars, builtin, name)
        if entry.get("source_type") == BUILTIN_FILTER:
            return (2, 0, 0, name)
        return (3, 0, 0, name)

    return sorted(entries, key=sort_key)


def build_robots_txt() -> str:
    return f"User-agent: *\nContent-Signal: search=yes, ai-input=yes, ai-train=yes\nAllow: /\n\nSitemap: {SITEMAP_URL}\n"


WEBSITE_ID = f"{SITE_URL}#website"
ISPARTOF_WEBSITE = {"@type": "WebSite", "@id": WEBSITE_ID}


def _website_node() -> dict:
    return {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "name": "Awesome Python",
        "url": SITE_URL,
        "inLanguage": "en",
        "sameAs": "https://github.com/vinta/awesome-python",
    }


def _item_list_payload(entries: Sequence[TemplateEntry]) -> dict:
    return {
        "@type": "ItemList",
        "numberOfItems": len(entries),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "name": entry["name"],
                "url": entry["url"],
            }
            for i, entry in enumerate(entries, start=1)
        ],
    }


def build_homepage_json_ld(entries: Sequence[TemplateEntry], total_categories: int) -> dict:
    description = (
        "An opinionated guide to the best Python frameworks, libraries, and tools. "
        f"Explore {len(entries)} curated projects across {total_categories} categories, "
        "from AI and agents to data science and web development."
    )
    return {
        "@context": "https://schema.org",
        "@graph": [
            _website_node(),
            {
                "@type": "CollectionPage",
                "@id": SITE_URL,
                "name": "Awesome Python",
                "url": SITE_URL,
                "description": description,
                "isPartOf": ISPARTOF_WEBSITE,
                "inLanguage": "en",
                "mainEntity": _item_list_payload(entries),
            },
        ],
    }


def category_meta_title(name: str, parent_name: str | None = None) -> str:
    if parent_name:
        # Lead with the section's title so the page matches searches like "python jwt library".
        title = f"{category_meta_title(parent_name).removesuffix(' - Awesome Python')}: {name}"
        # Google shows the site name above each result, so a long title drops it rather than get cut off.
        return f"{title} - Awesome Python" if len(title) <= 43 else title
    # Names ending in one of these nouns already say what the entries are.
    noun = "" if name.rsplit(" ", 1)[-1] in PLURAL_NOUNS else " Libraries"
    prefix = "" if name.startswith("Python ") else "Python "
    title = f"{prefix}{name}{noun} - Awesome Python"
    if len(title) <= 60:
        return title
    return f"{name} - Awesome Python"


def category_meta_description(name: str, entry_count: int, description: str) -> str:
    count_sentence = f"Explore {entry_count} curated Python project{'s' if entry_count != 1 else ''} in {name}."
    if description:
        lead = description if description.endswith((".", "!", "?")) else f"{description}."
        return f"{lead} {count_sentence}"
    return f"{count_sentence} Part of the Awesome Python list."


def subcategory_meta_description(name: str, parent_name: str, entry_names: Sequence[str]) -> str:
    names = entry_names[0] if len(entry_names) == 1 else f"{', '.join(entry_names[:-1])}{',' if len(entry_names) > 2 else ''} and {entry_names[-1]}"
    return f"The {name} picks in Awesome Python's {parent_name} list: {names}."


def entry_name_key(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def link_pick_names(pick: str, slugs_by_key: dict[str, str]) -> str:
    """Link entry names in a "How to choose" pick to their rows, preferring the longest match.

    Names match ignoring case and punctuation, so the README's PyPI-style
    "django-ninja" matches the intro's "Django Ninja".
    """
    words = list(re.finditer(r"`[^`]*`|[^\s,]+", pick))
    parts, pos, i = [], 0, 0
    while i < len(words):
        for j in range(min(len(words), i + 4), i, -1):
            start, end = words[i].start(), words[j - 1].end()
            span = pick[start:end]
            slug = slugs_by_key.get(entry_name_key(span))
            # Code spans and dangling punctuation like "Django -" stay outside links
            if slug and span[0].isalnum() and span[-1].isalnum() and "," not in span and "`" not in span:
                parts.append(f"{pick[pos:start]}[{span}](#entry-{slug})")
                pos, i = end, j
                break
        else:
            i += 1
    return "".join(parts) + pick[pos:]


def link_intro_picks(text: str, entry_names: Sequence[str]) -> str:
    """Link the picks in an intro's "How to choose:" list to their rows in the table below."""
    head, marker, rest = text.partition("\nHow to choose:\n\n")
    if not marker:
        return text
    slugs_by_key = {entry_name_key(name): slugify(name) for name in entry_names}
    for alias, name in PICK_ALIASES.items():
        if entry_name_key(name) in slugs_by_key:
            slugs_by_key[entry_name_key(alias)] = slugs_by_key[entry_name_key(name)]
    lines = rest.split("\n")
    for i, line in enumerate(lines):
        if not line.startswith("- "):
            break
        situation, _, pick = line.rpartition(": ")
        lines[i] = f"{situation}: {link_pick_names(pick, slugs_by_key)}"
    return head + marker + "\n".join(lines)


def load_category_intro(path: Path, entry_names: Sequence[str] = ()) -> tuple[str, str, str, str]:
    """Render a category intro file to HTML, split at the end of its "How to choose:" list.

    Returns the part shown above the table, the guide shown below it, and the
    first paragraph as plain text for the meta description and as HTML for
    group pages. A file without the list, like a one-project category's,
    keeps only its lead above the table.
    Returns empty strings if the category has no intro file.
    """
    if not path.exists():
        return "", "", "", ""
    md = MarkdownIt("commonmark")
    tokens = md.parse(link_intro_picks(path.read_text(encoding="utf-8"), entry_names))
    for token in tokens:
        for child in token.children or []:
            if child.type == "link_open" and not str(child.attrGet("href")).startswith("#"):
                child.attrSet("target", "_blank")
                child.attrSet("rel", "noopener")
    lead = next(node for node in SyntaxTreeNode(tokens).children if node.type == "paragraph")
    split_at = next(j for j, token in enumerate(tokens) if token.type == "paragraph_close" and token.level == 0) + 1
    for i, token in enumerate(tokens):
        if token.type == "inline" and token.level == 1 and token.content == "How to choose:" and i + 2 < len(tokens) and tokens[i + 2].type == "bullet_list_open":
            split_at = next(j for j in range(i + 3, len(tokens)) if tokens[j].type == "bullet_list_close" and tokens[j].level == 0) + 1
            break
    render = md.renderer.render
    return (
        render(tokens[:split_at], md.options, {}),
        render(tokens[split_at:], md.options, {}),
        render_inline_text(lead.children[0].children),
        render(lead.to_tokens(), md.options, {}),
    )


def group_section_entries(section: ParsedSection, entries_by_key: dict[tuple[str, str], TemplateEntry]) -> list[EntryGroup]:
    """Group a section's entries by use case (subcategory), both in README order."""
    groups: dict[str, EntryGroup] = {}
    for parsed in section["entries"]:
        name = parsed["subcategory"]
        slug = slugify(name) if name else ""
        group = groups.setdefault(name, EntryGroup(name=name, slug=slug, url=subcategory_path(section["slug"], slug) if name else "", lead="", entries=[]))
        group["entries"].append(entries_by_key[(parsed["url"], parsed["name"])])
    return list(groups.values())


def group_entries_by_section(sections: Sequence[ParsedSection], entries_by_key: dict[tuple[str, str], TemplateEntry], intros_dir: Path) -> list[EntryGroup]:
    """Group a thematic group's entries by section, both in README order, listing each entry once."""
    placed: set[tuple[str, str]] = set()
    groups: list[EntryGroup] = []
    for section in sections:
        entries: list[TemplateEntry] = []
        for parsed in section["entries"]:
            key = (parsed["url"], parsed["name"])
            if key not in placed:
                placed.add(key)
                entries.append(entries_by_key[key])
        groups.append(EntryGroup(name=section["name"], slug=section["slug"], url=category_path(section), lead=load_category_intro(intros_dir / f"{section['slug']}.md")[3], entries=entries))
    return groups


def build_breadcrumb_json_ld(items: Sequence[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "name": name,
                "item": url,
            }
            for i, (name, url) in enumerate(items, start=1)
        ],
    }


def build_category_json_ld(
    name: str,
    url: str,
    description: str,
    entries: Sequence[TemplateEntry],
    breadcrumbs: Sequence[tuple[str, str]],
) -> dict:
    return {
        "@context": "https://schema.org",
        "@graph": [
            _website_node(),
            {
                "@type": "CollectionPage",
                "@id": url,
                "name": name,
                "url": url,
                "description": description,
                "isPartOf": ISPARTOF_WEBSITE,
                "inLanguage": "en",
                "mainEntity": _item_list_payload(entries),
            },
            build_breadcrumb_json_ld(breadcrumbs),
        ],
    }


def build_sponsorship_json_ld() -> dict:
    return {
        "@context": "https://schema.org",
        "@graph": [
            _website_node(),
            {
                "@type": "WebPage",
                "@id": SPONSORSHIP_PUBLIC_URL,
                "name": "Sponsor Awesome Python",
                "url": SPONSORSHIP_PUBLIC_URL,
                "description": SPONSORSHIP_DESCRIPTION,
                "isPartOf": ISPARTOF_WEBSITE,
                "inLanguage": "en",
            },
            build_breadcrumb_json_ld(
                [
                    ("Awesome Python", SITE_URL),
                    ("Sponsorship", SPONSORSHIP_PUBLIC_URL),
                ]
            ),
        ],
    }


def category_path(category: ParsedSection) -> str:
    return f"/categories/{category['slug']}/"


def category_public_url(category: ParsedSection) -> str:
    return f"{SITE_URL}categories/{category['slug']}/"


def group_path(group_slug: str) -> str:
    return f"/categories/{group_slug}/"


def group_public_url(group_slug: str) -> str:
    return f"{SITE_URL}categories/{group_slug}/"


def subcategory_path(category_slug: str, subcategory_slug: str) -> str:
    return f"/categories/{category_slug}/{subcategory_slug}/"


def subcategory_public_url(category_slug: str, subcategory_slug: str) -> str:
    return f"{SITE_URL}categories/{category_slug}/{subcategory_slug}/"


def synthetic_category(name: str, slug: str) -> SyntheticCategory:
    return {"name": name, "slug": slug, "description": "", "description_html": ""}


def git_last_change_date(repo_root: Path, *log_args: str) -> str:
    """Return the date of the last commit matching `git log` args, or "" without git history."""
    result = subprocess.run(["git", "log", "-1", "--format=%cs", "--no-patch", *log_args], cwd=repo_root, capture_output=True, text=True, check=False)
    return result.stdout.strip()


def section_line_range(readme_text: str, name: str) -> str:
    """Return a section's README lines as a `git log -L` range, from its heading to the line before the next heading."""
    lines = readme_text.split("\n")
    start = next(i for i, line in enumerate(lines) if re.fullmatch(rf"#+ {re.escape(name)}", line))
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("#")), len(lines))
    return f"{start + 1},{end}:README.md"


def write_sitemap_xml(path: Path, urls: Sequence[tuple[str, str]]) -> None:
    ET.register_namespace("", SITEMAP_NS)
    urlset = ET.Element(f"{{{SITEMAP_NS}}}urlset")
    for url, lastmod in urls:
        url_el = ET.SubElement(urlset, f"{{{SITEMAP_NS}}}url")
        loc_el = ET.SubElement(url_el, f"{{{SITEMAP_NS}}}loc")
        loc_el.text = url
        lastmod_el = ET.SubElement(url_el, f"{{{SITEMAP_NS}}}lastmod")
        lastmod_el.text = lastmod

    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True)
    with path.open("ab") as f:
        f.write(b"\n")


def top_level_heading_text(line: str) -> str | None:
    stripped = line.strip()
    match = re.match(r"^(#{1,2})\s+(.+)$", stripped)
    if match is None:
        return None
    return match.group(2).strip().strip("#").strip().strip("*").strip()


def extract_categories_body(markdown: str) -> str:
    """Return content from `Categories` through `Projects`, excluding later sections."""
    lines = markdown.splitlines(keepends=True)
    start_idx = None
    end_idx = len(lines)
    for i, line in enumerate(lines):
        heading = top_level_heading_text(line)
        if heading is None:
            continue
        if start_idx is None and heading.lower() == "categories":
            start_idx = i + 1
            while start_idx < len(lines) and lines[start_idx].strip() == "":
                start_idx += 1
        elif start_idx is not None and heading.lower() in ("resources", "contributing"):
            end_idx = i
            break
    if start_idx is None:
        return ""
    return "".join(lines[start_idx:end_idx]).rstrip() + "\n"


def github_markdown_anchor(text: str) -> str:
    anchor = text.strip().lower()
    anchor = re.sub(r"[^\w\s-]", "", anchor)
    anchor = re.sub(r"\s", "-", anchor)
    return f"#{anchor}"


def link_llms_category_index_to_canonical_pages(markdown: str, categories: Sequence[ParsedSection]) -> str:
    """Point the README-derived category index at canonical category pages."""
    category_urls = {}
    for category in categories:
        public_url = category_public_url(category)
        category_urls[f"#{category['slug']}"] = public_url
        category_urls[github_markdown_anchor(category["name"])] = public_url
    lines = markdown.splitlines(keepends=True)
    out: list[str] = []

    def replace_link(match: re.Match[str]) -> str:
        target = match.group(2)
        url = category_urls.get(target)
        if url is None:
            return match.group(0)
        return match.group(0).replace(f"({target})", f"({url})", 1)

    for line in lines:
        out.append(MARKDOWN_LINK_RE.sub(replace_link, line))

    return "".join(out)


def link_description_anchors_to_category_pages(categories: Sequence[ParsedSection]) -> None:
    """Point README anchor links in section descriptions at category pages, which lack those anchors."""
    category_paths = {}
    for category in categories:
        category_paths[f"#{category['slug']}"] = category_path(category)
        category_paths[github_markdown_anchor(category["name"])] = category_path(category)

    def replace_attrs(match: re.Match[str]) -> str:
        path = category_paths.get(match.group(1))
        return f'href="{path}"' if path else match.group(0)

    for category in categories:
        category["description_html"] = ANCHOR_LINK_ATTRS_RE.sub(replace_attrs, category["description_html"])


def build_llms_txt(
    template_text: str,
    *,
    readme_text: str,
    subtitle: str,
    build_date: str,
    stars_data: dict[str, dict],
    downloads_data: dict[str, int],
    categories: Sequence[ParsedSection],
    total_entries: int,
) -> str:
    """Render the llms.txt entry point with the curated category shortlist."""
    categories_md = annotate_entries_with_stats(
        link_llms_category_index_to_canonical_pages(
            extract_categories_body(readme_text).rstrip(),
            categories,
        ),
        stars_data,
        downloads_data,
    )
    text_env = Environment(autoescape=False, trim_blocks=True, lstrip_blocks=True)
    rendered = text_env.from_string(template_text).render(
        subtitle=subtitle,
        build_date=build_date,
        site_url=SITE_URL,
        github_repo_url="https://github.com/vinta/awesome-python",
        contributing_url="https://github.com/vinta/awesome-python/blob/master/CONTRIBUTING.md",
        sponsorship_url=SPONSORSHIP_PUBLIC_URL,
        sitemap_url=SITEMAP_URL,
        categories_md=categories_md,
        total_entries=total_entries,
        total_categories=len(categories),
    )
    return rendered.rstrip() + "\n"


def annotate_entries_with_stats(
    markdown: str,
    stars_data: dict[str, dict],
    downloads_data: dict[str, int],
) -> str:
    """Append download and star counts to bullet entry lines.

    Downloads are looked up by the first link's display name (the same key the
    TSV cache uses); stars by the first GitHub link with known star data.
    """
    lines = markdown.splitlines(keepends=True)
    out: list[str] = []
    for line in lines:
        if not BULLET_LINE_RE.match(line):
            out.append(line)
            continue
        links = MARKDOWN_LINK_RE.findall(line)
        parts: list[str] = []
        if links:
            name, url = links[0]
            # Category-index bullets link into the site itself, and stdlib entries
            # would hit same-named PyPI backports (e.g. logging) — no counts for either.
            if not url.startswith((SITE_URL, "#")) and detect_source_type(url) != BUILTIN_FILTER:
                downloads = downloads_data.get(normalize(name))
                if downloads is not None:
                    parts.append(f"PyPI downloads/month: {downloads}")
        for _, url in links:
            repo_key = extract_github_repo(url)
            if not repo_key:
                continue
            entry = stars_data.get(repo_key)
            if entry and "stars" in entry:
                parts.append(f"GitHub stars: {entry['stars']}")
                break
        if not parts:
            out.append(line)
            continue
        stripped = line.rstrip("\n")
        ending = line[len(stripped) :]
        out.append(f"{stripped} ({', '.join(parts)}){ending}")
    return "".join(out)


def remove_sponsors_section(markdown: str) -> str:
    lines = markdown.splitlines(keepends=True)
    start_idx = None
    for i, line in enumerate(lines):
        heading = top_level_heading_text(line)
        if heading and heading.lower() == "sponsors":
            start_idx = i
            break

    if start_idx is None:
        return markdown

    end_idx = len(lines)
    for i, line in enumerate(lines[start_idx + 1 :], start=start_idx + 1):
        if top_level_heading_text(line):
            end_idx = i
            break

    return "".join(lines[:start_idx] + lines[end_idx:])


def extract_entries(
    categories: list[ParsedSection],
    groups: list[ParsedGroup],
) -> list[TemplateEntry]:
    """Flatten categories into individual library entries for table display.

    Entries appearing in multiple categories are merged into a single entry
    with lists of categories and groups.
    """
    cat_to_group = {cat["name"]: group["name"] for group in groups for cat in group["categories"]}

    seen: dict[tuple[str, str], TemplateEntry] = {}  # (url, name) -> entry
    entries: list[TemplateEntry] = []
    for cat in categories:
        group_name = cat_to_group.get(cat["name"], "Other")
        for entry in cat["entries"]:
            key = (entry["url"], entry["name"])
            existing = seen.get(key)
            if existing is None:
                existing = TemplateEntry(
                    name=entry["name"],
                    url=entry["url"],
                    description=entry["description"],
                    categories=[],
                    groups=[],
                    subcategories=[],
                    stars=None,
                    downloads=None,
                    owner=None,
                    last_commit_at=None,
                    source_type=detect_source_type(entry["url"]),
                    bundled=bool(BUNDLED_PREFIX_RE.match(entry["description"])),
                    badge=None,
                    also_see=entry["also_see"],
                )
                seen[key] = existing
                entries.append(existing)
            if cat["name"] not in existing["categories"]:
                existing["categories"].append(cat["name"])
            if group_name not in existing["groups"]:
                existing["groups"].append(group_name)
            subcat = entry["subcategory"]
            if subcat:
                scoped = f"{cat['name']} > {subcat}"
                if not any(s["value"] == scoped for s in existing["subcategories"]):
                    sub_slug = slugify(subcat)
                    existing["subcategories"].append(
                        TemplateSubcategory(
                            name=subcat,
                            value=scoped,
                            slug=sub_slug,
                            url=f"/categories/{cat['slug']}/{sub_slug}/",
                        )
                    )
    return entries


def build(repo_root: Path) -> None:
    """Main build: parse README, render single-page HTML via Jinja2 templates."""
    website = repo_root / "website"
    readme_text = (repo_root / "README.md").read_text(encoding="utf-8")

    subtitle = ""
    for line in readme_text.split("\n"):
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            subtitle = stripped
            break

    parsed_groups = parse_readme(readme_text)
    sponsors = parse_sponsors(readme_text)
    for sponsor in sponsors:
        sponsor["url"] = sponsor_website_url(sponsor["url"])

    categories = [cat for g in parsed_groups for cat in g["categories"]]
    cat_slugs = [cat["slug"] for cat in categories]
    group_slugs = [g["slug"] for g in parsed_groups]
    all_top_level_slugs = cat_slugs + group_slugs + [BUILTIN_SLUG]
    duplicates = {s for s, n in Counter(all_top_level_slugs).items() if n > 1}
    if duplicates:
        raise ValueError(f"slug collision in /categories/ namespace: {sorted(duplicates)}. Rename a category or group so their slugs differ.")
    link_description_anchors_to_category_pages(categories)
    total_entries = sum(c["entry_count"] for c in categories)
    entries = extract_entries(categories, parsed_groups)
    build_date = datetime.now(UTC)

    stars_data = load_stars(website / "data" / "github_stars.json")
    downloads_data = load_downloads(website / "data" / "pypi_downloads.tsv")
    pypi_badges = load_pypi_badges()

    repo_self = stars_data.get("vinta/awesome-python", {})
    repo_stars = None
    if "stars" in repo_self:
        stars_val = repo_self["stars"]
        repo_stars = f"{stars_val // 1000}k" if stars_val >= 1000 else str(stars_val)

    for entry in entries:
        repo_key = extract_github_repo(entry["url"])
        if not repo_key and entry.get("source_type") == BUILTIN_FILTER:
            repo_key = "python/cpython"
        if repo_key and repo_key in stars_data:
            sd = stars_data[repo_key]
            entry["stars"] = sd["stars"]
            entry["owner"] = sd["owner"]
            entry["last_commit_at"] = sd.get("last_commit_at", "")
        # Stdlib entries would hit same-named PyPI backports (e.g. asyncio), not the stdlib.
        if entry.get("source_type") != BUILTIN_FILTER:
            entry["downloads"] = downloads_data.get(normalize(entry["name"]))
        entry["badge"] = pypi_badges.get(normalize(entry["name"]))

    entries = sort_entries(entries)
    category_urls = {cat["name"]: category_path(cat) for cat in categories}

    filter_urls: dict[str, str] = dict(category_urls)
    for group in parsed_groups:
        filter_urls[group["name"]] = group_path(group["slug"])
    builtin_entries = [e for e in entries if e.get("source_type") == BUILTIN_FILTER]

    env = Environment(
        loader=FileSystemLoader(website / "templates"),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["slugify"] = slugify
    site_dir = website / "output"
    if site_dir.exists():
        shutil.rmtree(site_dir)
    site_dir.mkdir(parents=True)

    homepage_json_ld = json.dumps(
        build_homepage_json_ld(entries, len(categories)),
        ensure_ascii=False,
    ).replace("</", "<\\/")

    tpl_index = env.get_template("index.html")
    (site_dir / "index.html").write_text(
        tpl_index.render(
            categories=categories,
            subtitle=subtitle,
            entries=entries,
            total_entries=total_entries,
            total_categories=len(categories),
            repo_stars=repo_stars,
            sponsors=sponsors,
            category_urls=category_urls,
            filter_urls=filter_urls,
            homepage_json_ld=homepage_json_ld,
        ),
        encoding="utf-8",
    )

    tpl_category = env.get_template("category.html")
    categories_dir = site_dir / "categories"

    def render_category(
        category: TemplateCategory,
        *,
        category_url: str,
        entries: Sequence[TemplateEntry],
        current_path: str,
        page_dir: Path,
        parent_category: ParsedSection | None = None,
        group_categories: Sequence[ParsedSection] | None = None,
        entry_groups: Sequence[EntryGroup] = (),
    ) -> None:
        page_dir.mkdir(parents=True, exist_ok=True)
        parent_name = parent_category["name"] if parent_category else None
        category_title = category_meta_title(category["name"], parent_name)
        page_entries = [entry for group in entry_groups for entry in group["entries"]] if entry_groups else entries
        intro_html, guide_html, intro_lead, _ = load_category_intro(
            website / "data" / "category_intros" / f"{current_path.removeprefix('/categories/').strip('/')}.md", [e["name"] for e in page_entries]
        )
        if intro_lead:
            category_description = intro_lead
        elif parent_name:
            category_description = subcategory_meta_description(category["name"], parent_name, [e["name"] for e in entries])
        else:
            category_description = category_meta_description(category["name"], len(entries), category["description"])
        breadcrumbs = [("Awesome Python", SITE_URL)]
        if parent_category:
            breadcrumbs.append((parent_category["name"], category_public_url(parent_category)))
        breadcrumbs.append((category["name"], category_url))
        category_json_ld = json.dumps(
            build_category_json_ld(category_title.removesuffix(" - Awesome Python"), category_url, category_description, page_entries, breadcrumbs),
            ensure_ascii=False,
        ).replace("</", "<\\/")
        (page_dir / "index.html").write_text(
            tpl_category.render(
                category=category,
                category_title=category_title,
                category_url=category_url,
                category_description=category_description,
                intro_html=intro_html,
                guide_html=guide_html,
                entries=entries,
                entry_groups=entry_groups,
                total_categories=len(categories),
                category_urls=category_urls,
                current_path=current_path,
                filter_urls=filter_urls,
                parent_category=parent_category,
                group_categories=group_categories,
                category_json_ld=category_json_ld,
                sponsors=sponsors,
            ),
            encoding="utf-8",
        )

    entries_by_key = {(e["url"], e["name"]): e for e in entries}
    section_groups = {category["name"]: group_section_entries(category, entries_by_key) for category in categories}
    for category in categories:
        render_category(
            category,
            category_url=category_public_url(category),
            entries=[e for e in entries if category["name"] in e["categories"]],
            current_path=category_path(category),
            page_dir=categories_dir / category["slug"],
            entry_groups=section_groups[category["name"]],
        )

    for group in parsed_groups:
        render_category(
            synthetic_category(group["name"], group["slug"]),
            category_url=group_public_url(group["slug"]),
            entries=[e for e in entries if group["name"] in e["groups"]],
            current_path=group_path(group["slug"]),
            page_dir=categories_dir / group["slug"],
            group_categories=group["categories"],
            entry_groups=group_entries_by_section(group["categories"], entries_by_key, website / "data" / "category_intros"),
        )

    if builtin_entries:
        render_category(
            synthetic_category(BUILTIN_FILTER, BUILTIN_SLUG),
            category_url=BUILTIN_PUBLIC_URL,
            entries=builtin_entries,
            current_path=BUILTIN_PATH,
            page_dir=categories_dir / BUILTIN_SLUG,
        )

    sponsorship_dir = site_dir / "sponsorship"
    sponsorship_dir.mkdir(parents=True, exist_ok=True)
    tpl_sponsorship = env.get_template("sponsorship.html")
    hero_stats: list[str] = []
    if repo_stars:
        hero_stats.append(f"{repo_stars}+ stars on GitHub")
    (sponsorship_dir / "index.html").write_text(
        tpl_sponsorship.render(
            hero_stats=hero_stats,
            sponsorship_description=SPONSORSHIP_DESCRIPTION,
            sponsorship_json_ld=json.dumps(build_sponsorship_json_ld(), ensure_ascii=False).replace("</", "<\\/"),
        ),
        encoding="utf-8",
    )

    subcat_to_entries: dict[str, list[TemplateEntry]] = {}
    subcat_meta: dict[str, tuple[str, str, str]] = {}  # value -> (cat_slug, sub_slug, sub_name)
    cat_slug_by_url_prefix = {f"/categories/{c['slug']}/": c["slug"] for c in categories}
    cat_by_slug = {c["slug"]: c for c in categories}
    for entry in entries:
        for sub in entry.get("subcategories", []):
            value = sub["value"]
            subcat_to_entries.setdefault(value, []).append(entry)
            if value not in subcat_meta:
                for prefix, cat_slug in cat_slug_by_url_prefix.items():
                    if sub["url"].startswith(prefix):
                        subcat_meta[value] = (cat_slug, sub["slug"], sub["name"])
                        break

    for value, (cat_slug, sub_slug, sub_name) in subcat_meta.items():
        render_category(
            synthetic_category(sub_name, sub_slug),
            category_url=subcategory_public_url(cat_slug, sub_slug),
            entries=subcat_to_entries[value],
            current_path=subcategory_path(cat_slug, sub_slug),
            page_dir=categories_dir / cat_slug / sub_slug,
            parent_category=cat_by_slug[cat_slug],
            entry_groups=[EntryGroup(name="", slug="", url="", lead="", entries=group["entries"]) for group in section_groups[cat_by_slug[cat_slug]["name"]] if group["name"] == sub_name],
        )

    redirects_file = website / "data" / "redirects.json"
    redirects = json.loads(redirects_file.read_text(encoding="utf-8")) if redirects_file.exists() else {}
    for old_path, new_path in redirects.items():
        tpl_redirect = env.get_template("redirect.html")
        stub = site_dir / old_path.strip("/") / "index.html"
        if stub.exists():
            raise ValueError(f"redirect source {old_path} is a live page; remove it from redirects.json")
        if not (site_dir / new_path.strip("/") / "index.html").exists():
            raise ValueError(f"redirect target {new_path} for {old_path} does not exist")
        stub.parent.mkdir(parents=True, exist_ok=True)
        stub.write_text(tpl_redirect.render(target_url=SITE_URL + new_path.lstrip("/")), encoding="utf-8")

    static_src = website / "static"
    static_dst = site_dir / "static"
    if static_src.exists():
        shutil.copytree(static_src, static_dst, dirs_exist_ok=True)

    llms_template = (website / "templates" / "llms.txt").read_text(encoding="utf-8")
    llms_txt = build_llms_txt(
        llms_template,
        readme_text=readme_text,
        subtitle=subtitle,
        build_date=build_date.date().isoformat(),
        stars_data=stars_data,
        downloads_data=downloads_data,
        categories=categories,
        total_entries=total_entries,
    )
    (site_dir / "robots.txt").write_text(build_robots_txt(), encoding="utf-8")
    # Daily star and download refreshes are not significant changes, so lastmod follows commits to the page's own content.
    build_day = build_date.date().isoformat()
    readme_date = git_last_change_date(repo_root, "--", "README.md") or build_day
    section_dates = {
        c["slug"]: max(
            git_last_change_date(repo_root, "-L", section_line_range(readme_text, c["name"])),
            git_last_change_date(repo_root, "--", f"website/data/category_intros/{c['slug']}.md"),
        )
        or build_day
        for c in categories
    }
    sitemap_urls = [(SITE_URL, readme_date)]
    sitemap_urls.extend((category_public_url(c), section_dates[c["slug"]]) for c in categories)
    sitemap_urls.extend((group_public_url(g["slug"]), max(section_dates[c["slug"]] for c in g["categories"])) for g in parsed_groups)
    if builtin_entries:
        sitemap_urls.append((BUILTIN_PUBLIC_URL, readme_date))
    for cat_slug, sub_slug, _ in sorted(subcat_meta.values()):
        sitemap_urls.append((subcategory_public_url(cat_slug, sub_slug), section_dates[cat_slug]))
    sitemap_urls.append((SPONSORSHIP_PUBLIC_URL, git_last_change_date(repo_root, "--", "SPONSORSHIP.md") or build_day))
    write_sitemap_xml(site_dir / "sitemap.xml", sitemap_urls)
    (site_dir / "llms.txt").write_text(llms_txt, encoding="utf-8")

    print(f"Built site with {len(parsed_groups)} groups, {len(categories)} categories")
    print(f"Total entries: {total_entries}")
    print(f"Output: {site_dir}")


if __name__ == "__main__":
    build(Path(__file__).parent.parent)



================================================
FILE: website/fetch_github_stars.py
================================================
#!/usr/bin/env python3
"""Fetch GitHub star counts and owner info for all GitHub repos in README.md.

The output file (data/github_stars.json) is gitignored; CI fetches it at
deploy time, so local runs are for previews only — never commit the data.
Entries removed from README.md leave harmless orphan keys behind.
"""

import json
import os
import re
import sys
from collections.abc import Sequence
from datetime import UTC, datetime, timedelta
from itertools import batched
from pathlib import Path

import httpx

from build import extract_github_repo, load_stars

CACHE_MAX_AGE_HOURS = 12
DATA_DIR = Path(__file__).parent / "data"
CACHE_FILE = DATA_DIR / "github_stars.json"
README_PATH = Path(__file__).parent.parent / "README.md"
GRAPHQL_URL = "https://api.github.com/graphql"
BATCH_SIZE = 50

# GitHub usernames: alphanumeric and hyphens, must start/end with alphanumeric.
GITHUB_OWNER_RE = re.compile(r"^[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?$")
# GitHub repo names: alphanumeric, hyphens, underscores, dots, must start with alphanumeric.
GITHUB_NAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]*$")


def extract_github_repos(text: str) -> set[str]:
    """Extract unique owner/repo pairs from GitHub URLs in markdown text."""
    repos = set()
    for url in re.findall(r"https?://github\.com/[^\s)\]]+", text):
        repo = extract_github_repo(url.split("#")[0].rstrip("/"))
        if repo:
            repos.add(repo)
    return repos


def save_cache(cache: dict) -> None:
    """Write the star cache to disk, creating data/ dir if needed."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def build_graphql_query(repos: Sequence[str]) -> str:
    """Build a GraphQL query with aliases for up to 100 repos."""
    parts = []
    for i, repo in enumerate(repos):
        owner, name = repo.split("/", 1)
        if not GITHUB_OWNER_RE.match(owner) or not GITHUB_NAME_RE.match(name):
            continue
        parts.append(f'repo_{i}: repository(owner: "{owner}", name: "{name}") {{ stargazerCount owner {{ login }} defaultBranchRef {{ target {{ ... on Commit {{ committedDate }} }} }} }}')
    if not parts:
        return ""
    return "query { " + " ".join(parts) + " }"


def parse_graphql_response(
    data: dict,
    repos: Sequence[str],
) -> dict[str, dict]:
    """Parse GraphQL response into {owner/repo: {stars, owner}} dict."""
    result = {}
    for i, repo in enumerate(repos):
        node = data.get(f"repo_{i}")
        if node is None:
            continue
        default_branch = node.get("defaultBranchRef") or {}
        target = default_branch.get("target") or {}
        result[repo] = {
            "stars": node.get("stargazerCount", 0),
            "owner": node.get("owner", {}).get("login", ""),
            "last_commit_at": target.get("committedDate", ""),
        }
    return result


def fetch_batch(repos: Sequence[str], client: httpx.Client) -> dict[str, dict]:
    """Fetch star data for a batch of repos via GitHub GraphQL API."""
    query = build_graphql_query(repos)
    if not query:
        return {}
    resp = client.post(GRAPHQL_URL, json={"query": query})
    resp.raise_for_status()
    result = resp.json()
    if "errors" in result:
        for err in result["errors"]:
            print(f"  Warning: {err.get('message', err)}", file=sys.stderr)
    data = result.get("data", {})
    return parse_graphql_response(data, repos)


def main() -> None:
    """Fetch GitHub stars for all repos in README.md, updating the JSON cache."""
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("Error: GITHUB_TOKEN environment variable is required.", file=sys.stderr)
        sys.exit(1)

    readme_text = README_PATH.read_text(encoding="utf-8")
    current_repos = extract_github_repos(readme_text)
    current_repos.add("vinta/awesome-python")
    print(f"Found {len(current_repos)} GitHub repos in README.md")

    cache = load_stars(CACHE_FILE)
    now = datetime.now(UTC)

    # Prune entries not in current README
    pruned = {k: v for k, v in cache.items() if k in current_repos}
    if len(pruned) < len(cache):
        print(f"Pruned {len(cache) - len(pruned)} stale cache entries")
    cache = pruned

    # Determine which repos need fetching (missing or stale)
    max_age = timedelta(hours=CACHE_MAX_AGE_HOURS)
    to_fetch = []
    for repo in sorted(current_repos):
        entry = cache.get(repo)
        if entry and "fetched_at" in entry:
            fetched = datetime.fromisoformat(entry["fetched_at"])
            if now - fetched < max_age:
                continue
        to_fetch.append(repo)

    print(f"{len(to_fetch)} repos to fetch ({len(current_repos) - len(to_fetch)} cached)")

    if not to_fetch:
        save_cache(cache)
        print("Cache is up to date.")
        return

    # Fetch in batches
    fetched_count = 0
    skipped_repos: list[str] = []

    now_iso = now.isoformat()
    total_batches = (len(to_fetch) + BATCH_SIZE - 1) // BATCH_SIZE

    with httpx.Client(
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
        transport=httpx.HTTPTransport(retries=2),
        timeout=30,
    ) as client:
        for batch_num, batch in enumerate(batched(to_fetch, BATCH_SIZE), 1):
            print(f"Fetching batch {batch_num}/{total_batches} ({len(batch)} repos)...")

            try:
                results = fetch_batch(batch, client)
            except httpx.HTTPStatusError as e:
                print(f"HTTP error {e.response.status_code}", file=sys.stderr)
                if e.response.status_code == 401:
                    print("Error: Invalid GITHUB_TOKEN.", file=sys.stderr)
                    sys.exit(1)
                print("Saving partial cache and exiting.", file=sys.stderr)
                save_cache(cache)
                sys.exit(1)

            for repo in batch:
                if repo in results:
                    cache[repo] = {**results[repo], "fetched_at": now_iso}
                    fetched_count += 1
                else:
                    skipped_repos.append(repo)

            # Save after each batch in case of interruption
            save_cache(cache)

    if skipped_repos:
        print(f"Skipped {len(skipped_repos)} repos (deleted/private/renamed)")
    print(f"Done. Fetched {fetched_count} repos, {len(cache)} total cached.")


if __name__ == "__main__":
    main()



================================================
FILE: website/fetch_pypi_downloads_via_bigquery.py
================================================
#!/usr/bin/env python3
"""Cross-check last-30-day PyPI download counts for given names via BigQuery.

Queries the canonical source ClickPy mirrors —
`bigquery-public-data.pypi.file_downloads` via the `bq` CLI — and prints
name<TAB>count TSV to stdout. Names resolve through
data/pypi_name_overrides.json, matching the cache sweep. Maintainer-local (needs a personal GCP
account) and print-only: data/pypi_downloads.tsv is written solely by
fetch_pypi_downloads_via_clickpy.py.

Targeted cross-checks only — full-README sweeps belong to ClickPy. The
dry-run scan estimate scales with the IN list (measured 2026-08-16:
~38 GB for 2 names, ~275 GB for 53, ~1.2 TB for the full README — past
both MAX_BYTES_BILLED and the 1 TiB/month free tier), and BigQuery
enforces MAX_BYTES_BILLED against that pre-run estimate, so oversized
name lists fail before billing. Actual billed bytes come in far lower
via cluster pruning (33.7 GB for a single name). The table is
partitioned on timestamp and clustered on the top-level `project`
column — filter on `project`, never `file.project`: both hold identical
values (verified 2026-08-16, 408M rows on one day, zero mismatches), but
only a `project` filter gets cluster pruning, and the `file` record
costs ~4x more to scan. Always --dry-run first to check the estimate.

Usage: python fetch_pypi_downloads_via_bigquery.py [--dry-run] NAME [NAME ...]
"""

import subprocess
import sys
from json import loads

from fetch_pypi_downloads_via_clickpy import resolve

MAX_BYTES_BILLED = 400_000_000_000


def fetch_bigquery(names: list[str], dry_run: bool) -> dict[str, int]:
    in_list = ", ".join(f"'{name}'" for name in names)
    query = (
        "SELECT project, COUNT(*) AS downloads "
        "FROM `bigquery-public-data.pypi.file_downloads` "
        "WHERE DATE(timestamp) BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) "
        "AND CURRENT_DATE() "
        f"AND project IN ({in_list}) "
        "GROUP BY project"
    )
    cmd = ["bq", "query", "--use_legacy_sql=false", "--format=json", f"--maximum_bytes_billed={MAX_BYTES_BILLED}"]
    if dry_run:
        cmd.append("--dry_run")
    cmd.append(query)
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    if dry_run:
        print(result.stdout.strip() or result.stderr.strip())
        sys.exit(0)
    rows = loads(result.stdout)
    return {row["project"]: int(row["downloads"]) for row in rows}


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    names = set()
    for arg in sys.argv[1:]:
        if arg == "--dry-run":
            continue
        pkg = resolve(arg)
        if pkg is None:
            print(f"{arg}: not pip-installable per pypi_name_overrides.json, skipping", file=sys.stderr)
        else:
            names.add(pkg)
    names = sorted(names)
    if not names:
        print("Usage: python fetch_pypi_downloads_via_bigquery.py [--dry-run] NAME [NAME ...]", file=sys.stderr)
        sys.exit(1)
    counts = fetch_bigquery(names, dry_run)
    for name in names:
        print(f"{name}\t{counts.get(name, 'NOT_FOUND')}")


if __name__ == "__main__":
    main()



================================================
FILE: website/fetch_pypi_downloads_via_clickpy.py
================================================
#!/usr/bin/env python3
"""Fetch last-30-day PyPI download counts for all README entries via ClickPy.

ClickPy is ClickHouse's public mirror of the PyPI download dataset
(sql-clickhouse.clickhouse.com, user `demo`, no key, no personal
account): one batched query covers the full README in under a second.
Playground limits — 60 queries/hour/IP, 1000 result rows — sit far above
a full-README sweep. The per-day table is a SummingMergeTree, so the
query must sum(count) GROUP BY, never count raw rows. Counts include
mirror/CI traffic; never mix these figures with pypistats.org, which
excludes mirrors by default.

This script is the sole writer of data/pypi_downloads.tsv and rewrites it
from scratch each run, so entries removed from README.md drop out
naturally; names with no PyPI rows are written as NOT_FOUND. Counts are
looked up by README display name; when the display name differs from the
canonical PyPI package (a squatter or a dead predecessor would be
measured otherwise), add the mapping to the curated
data/pypi_name_overrides.json — normalized README name to
{"package": ..., "reason": ...}, where package is the real PyPI name
or null for projects that are not pip-installable so their row is
never queried, and reason records why. The file starts with a header row (name, package,
downloads, fetched_at) — package is the PyPI package the row actually
measured ("-" for null overrides) — and every row carries the sweep
date: a cache fetched within the last 7 days is current enough for
audit verdicts, so only re-run when older. Cross-checks against other
sources (fetch_pypi_downloads_via_bigquery.py,
fetch_pypi_downloads_via_pepy.py) print to stdout and never touch the
cache.

Usage: python fetch_pypi_downloads_via_clickpy.py
"""

import json
import re
from datetime import UTC, datetime
from pathlib import Path

import httpx

from readme_parser import parse_readme

DATA_DIR = Path(__file__).parent / "data"
OUT_FILE = DATA_DIR / "pypi_downloads.tsv"
OVERRIDES_FILE = DATA_DIR / "pypi_name_overrides.json"
README_PATH = Path(__file__).parent.parent / "README.md"
CLICKPY_URL = "https://sql-clickhouse.clickhouse.com/?user=demo"

# PyPI normalizes names to lowercase with runs of -, _, . collapsed to -.
PYPI_NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")


def normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name.lower())


def load_overrides() -> dict[str, str | None]:
    """Load curated overrides: normalized README name -> PyPI package to measure (None = never query).

    Each file entry is {"package": str | null, "reason": str | null} plus an
    optional "badge" the website renders in place of a download count; the
    reason is documentation only — required for null packages, optional for
    remaps.
    """
    raw = json.loads(OVERRIDES_FILE.read_text())
    return {name: entry["package"] for name, entry in raw.items()}


def resolve(name: str) -> str | None:
    """Map a README display name to the PyPI package to measure. None = not pip-installable."""
    normalized = normalize(name)
    return load_overrides().get(normalized, normalized)


def collect_names(readme_text: str) -> list[str]:
    names = set()
    for group in parse_readme(readme_text):
        for section in group["categories"]:
            for entry in section["entries"]:
                normalized = normalize(entry["name"])
                if PYPI_NAME_RE.match(normalized):
                    names.add(normalized)
    return sorted(names)


def fetch_clickpy(names: list[str]) -> dict[str, int]:
    in_list = ", ".join(f"'{name}'" for name in names)
    query = f"SELECT project, sum(count) AS downloads FROM pypi.pypi_downloads_per_day WHERE project IN ({in_list}) AND date >= today() - 30 GROUP BY project FORMAT JSON"
    resp = httpx.post(CLICKPY_URL, content=query, timeout=60)
    resp.raise_for_status()
    return {row["project"]: int(row["downloads"]) for row in resp.json()["data"]}


def main() -> None:
    names = collect_names(README_PATH.read_text())
    overrides = load_overrides()
    packages = {name: overrides.get(name, name) for name in names}
    query_names = sorted({pkg for pkg in packages.values() if pkg})
    print(f"Querying {len(query_names)} package names...")
    counts = fetch_clickpy(query_names)
    fetched_at = datetime.now(UTC).date().isoformat()
    rows = "\n".join(f"{name}\t{pkg or '-'}\t{counts.get(pkg, 'NOT_FOUND') if pkg else 'NOT_FOUND'}\t{fetched_at}" for name, pkg in packages.items())
    OUT_FILE.write_text(f"name\tpackage\tdownloads\tfetched_at\n{rows}\n")
    print(f"Done. {len(counts)}/{len(query_names)} names found on PyPI. Cached to {OUT_FILE}")


if __name__ == "__main__":
    main()



================================================
FILE: website/fetch_pypi_downloads_via_pepy.py
================================================
#!/usr/bin/env python3
"""Spot-check last-30-day PyPI download counts via the pepy.tech API.

Cross-check for a handful of packages during audits — not for full-README
sweeps: the free API key is throttled to 5 requests/minute (10 burst), so
this script sleeps 12s between requests and 530 names would take ~2 hours
(use fetch_pypi_downloads_via_clickpy.py for bulk). Reads PEPY_TECH_API_KEY from the
environment, falling back to the repo-root .env. The v2 endpoint returns
~90 days of per-day per-version counts; this script sums the most recent
30 days present in the response across all versions. Names resolve
through data/pypi_name_overrides.json, matching the cache sweep. pepy counts include
mirror/CI traffic (CI filtering is a paid pepy feature), matching the
ClickPy/BigQuery figures; pypistats.org excludes mirrors, so never mix
the two in one comparison. Results print to stdout as TSV and are not
cached — data/pypi_downloads.tsv stays single-source.

Usage: python fetch_pypi_downloads_via_pepy.py NAME [NAME ...]
"""

import os
import sys
import time
from pathlib import Path

import httpx

from fetch_pypi_downloads_via_clickpy import resolve

ENV_FILE = Path(__file__).parent.parent / ".env"
PEPY_URL = "https://api.pepy.tech/api/v2/projects/{name}"
SECONDS_BETWEEN_REQUESTS = 12


def load_api_key() -> str:
    key = os.environ.get("PEPY_TECH_API_KEY", "")
    if not key and ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            name, sep, value = line.partition("=")
            if sep and name.strip() == "PEPY_TECH_API_KEY":
                key = value.strip()
    if not key:
        print("Error: PEPY_TECH_API_KEY not set (environment or repo-root .env).", file=sys.stderr)
        sys.exit(1)
    return key


def last_30_day_total(downloads_per_day: dict[str, dict[str, int]]) -> int:
    recent_days = sorted(downloads_per_day)[-30:]
    return sum(sum(downloads_per_day[day].values()) for day in recent_days)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python fetch_pypi_downloads_via_pepy.py NAME [NAME ...]", file=sys.stderr)
        sys.exit(1)
    names = []
    for arg in sys.argv[1:]:
        pkg = resolve(arg)
        if pkg is None:
            print(f"{arg}: not pip-installable per pypi_name_overrides.json, skipping", file=sys.stderr)
        else:
            names.append(pkg)
    with httpx.Client(headers={"X-API-Key": load_api_key()}, timeout=30) as client:
        for i, name in enumerate(names):
            if i:
                time.sleep(SECONDS_BETWEEN_REQUESTS)
            resp = client.get(PEPY_URL.format(name=name))
            if resp.status_code == 404:
                print(f"{name}\tNOT_FOUND")
                continue
            resp.raise_for_status()
            print(f"{name}\t{last_30_day_total(resp.json()['downloads'])}")


if __name__ == "__main__":
    main()



================================================
FILE: website/readme_parser.py
================================================
"""Parse README.md into structured section data using markdown-it-py AST.

Empirically verified behavior worth knowing before editing README.md:
everything above `## Projects` is ignored; new subcategories need no
parser change (a bullet without a leading link plus indented entries);
a standalone all-bold paragraph inside the Projects region becomes a
Thematic Group marker; prose placed right after `## Categories` leaks
into llms.txt; the build's "Total entries" figure counts sub-items
(indented links under an entry), not just entries.
"""

from __future__ import annotations

import re
from typing import TypedDict

from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
from markupsafe import escape


class AlsoSee(TypedDict):
    name: str
    url: str


class ParsedEntry(TypedDict):
    name: str
    url: str
    description: str  # inline HTML, properly escaped
    also_see: list[AlsoSee]
    subcategory: str  # sub-category label, empty if none


class ParsedSection(TypedDict):
    name: str
    slug: str
    description: str  # plain text, links resolved to text
    description_html: str  # inline HTML, properly escaped
    entries: list[ParsedEntry]
    entry_count: int


class ParsedGroup(TypedDict):
    name: str
    slug: str
    categories: list[ParsedSection]


class ParsedSponsor(TypedDict):
    name: str
    url: str
    description: str  # inline HTML, properly escaped


# --- Slugify ----------------------------------------------------------------

_SLUG_NON_ALNUM_RE = re.compile(r"[^a-z0-9\s-]")
_SLUG_WHITESPACE_RE = re.compile(r"[\s]+")
_SLUG_MULTI_DASH_RE = re.compile(r"-+")


def slugify(name: str) -> str:
    """Convert a category name to a URL-friendly slug."""
    slug = name.lower()
    slug = _SLUG_NON_ALNUM_RE.sub("", slug)
    slug = _SLUG_WHITESPACE_RE.sub("-", slug.strip())
    slug = _SLUG_MULTI_DASH_RE.sub("-", slug)
    return slug


# --- Inline renderers -------------------------------------------------------


def _render_inline(children: list[SyntaxTreeNode], *, html: bool) -> str:
    """Render inline AST nodes to HTML or plain text."""
    parts: list[str] = []
    for child in children:
        match child.type:
            case "text":
                parts.append(str(escape(child.content)) if html else child.content)
            case "html_inline":
                if html:
                    parts.append(str(escape(child.content)))
            case "softbreak":
                parts.append(" ")
            case "code_inline":
                parts.append(f"<code>{escape(child.content)}</code>" if html else child.content)
            case "link":
                inner = _render_inline(child.children, html=html)
                if html:
                    href = str(escape(_href(child)))
                    parts.append(f'<a href="{href}" target="_blank" rel="noopener">{inner}</a>')
                else:
                    parts.append(inner)
            case "em":
                inner = _render_inline(child.children, html=html)
                parts.append(f"<em>{inner}</em>" if html else inner)
            case "strong":
                inner = _render_inline(child.children, html=html)
                parts.append(f"<strong>{inner}</strong>" if html else inner)
    return "".join(parts)


def render_inline_html(children: list[SyntaxTreeNode]) -> str:
    """Render inline AST nodes to HTML with proper escaping."""
    return _render_inline(children, html=True)


def render_inline_text(children: list[SyntaxTreeNode]) -> str:
    """Render inline AST nodes to plain text (links become their text)."""
    return _render_inline(children, html=False)


# --- AST helpers -------------------------------------------------------------


def _heading_text(node: SyntaxTreeNode) -> str:
    """Extract plain text from a heading node."""
    for child in node.children:
        if child.type == "inline":
            return render_inline_text(child.children)
    return ""


def _heading_level(node: SyntaxTreeNode) -> int | None:
    """Return the numeric level for a heading node."""
    if node.type != "heading" or not node.tag.startswith("h"):
        return None
    return int(node.tag[1:])


def _extract_description_children(nodes: list[SyntaxTreeNode]) -> list[SyntaxTreeNode]:
    """Extract description children from the first paragraph if it's a single <em> block.

    Pattern: _Libraries for foo._ -> "Libraries for foo."
    """
    if not nodes:
        return []
    first = nodes[0]
    if first.type != "paragraph":
        return []
    for child in first.children:
        if child.type == "inline" and len(child.children) == 1:
            em = child.children[0]
            if em.type == "em":
                return em.children
    return []


# --- Entry extraction --------------------------------------------------------

_DESC_SEP_RE = re.compile(r"^\s*[-\u2013\u2014]\s*")
_SUBCAT_TRAILING_RE = re.compile(r"[\s,\-\u2013\u2014]+(also\s+see\s*)?$", re.IGNORECASE)


def _find_child(node: SyntaxTreeNode, child_type: str) -> SyntaxTreeNode | None:
    """Find first direct child of a given type."""
    for child in node.children:
        if child.type == child_type:
            return child
    return None


def _href(link: SyntaxTreeNode) -> str:
    """Return the link's href attribute as a string, or '' if missing."""
    href = link.attrGet("href")
    return href if isinstance(href, str) else ""


def _find_inline(node: SyntaxTreeNode) -> SyntaxTreeNode | None:
    """Find the inline node in a list_item's paragraph."""
    para = _find_child(node, "paragraph")
    if para is None:
        return None
    return _find_child(para, "inline")


def _extract_description_html(inline: SyntaxTreeNode, first_link: SyntaxTreeNode) -> str:
    """Extract description HTML from inline content after the first link.

    AST: [link("name"), text(" - Description.")]  ->  "Description."
    The separator (- / en-dash / em-dash) is stripped.
    """
    link_idx = next((i for i, c in enumerate(inline.children) if c is first_link), None)
    if link_idx is None:
        return ""
    desc_children = inline.children[link_idx + 1 :]
    if not desc_children:
        return ""
    html = render_inline_html(desc_children)
    return _DESC_SEP_RE.sub("", html)


def _parse_list_entries(
    bullet_list: SyntaxTreeNode,
    *,
    subcategory: str = "",
) -> list[ParsedEntry]:
    """Extract entries from a bullet_list AST node.

    Handles three patterns:
    - Text-only list_item -> subcategory label -> recurse into nested list
    - Link list_item with nested link-only items -> entry with also_see
    - Link list_item without nesting -> simple entry
    """
    entries: list[ParsedEntry] = []

    for list_item in bullet_list.children:
        if list_item.type != "list_item":
            continue

        inline = _find_inline(list_item)
        if inline is None:
            continue

        first_link = _find_child(inline, "link")

        if first_link is None or inline.children[0] is not first_link:
            # Subcategory label: take text before the first link, strip trailing separators
            pre_link = []
            for child in inline.children:
                if child.type == "link":
                    break
                pre_link.append(child)
            label = _SUBCAT_TRAILING_RE.sub("", render_inline_text(pre_link)) if pre_link else render_inline_text(inline.children)
            nested = _find_child(list_item, "bullet_list")
            if nested:
                entries.extend(_parse_list_entries(nested, subcategory=label))
            continue

        # Entry with a link
        name = render_inline_text(first_link.children)
        url = _href(first_link)
        desc_html = _extract_description_html(inline, first_link)

        # Collect also_see from nested bullet_list
        also_see: list[AlsoSee] = []
        nested = _find_child(list_item, "bullet_list")
        if nested:
            for sub_item in nested.children:
                if sub_item.type != "list_item":
                    continue
                sub_inline = _find_inline(sub_item)
                if sub_inline:
                    sub_link = _find_child(sub_inline, "link")
                    if sub_link:
                        also_see.append(
                            AlsoSee(
                                name=render_inline_text(sub_link.children),
                                url=_href(sub_link),
                            )
                        )

        entries.append(
            ParsedEntry(
                name=name,
                url=url,
                description=desc_html,
                also_see=also_see,
                subcategory=subcategory,
            )
        )

    return entries


def _parse_section_entries(content_nodes: list[SyntaxTreeNode]) -> list[ParsedEntry]:
    """Extract all entries from a section's content nodes."""
    entries: list[ParsedEntry] = []
    for node in content_nodes:
        if node.type == "bullet_list":
            entries.extend(_parse_list_entries(node))
    return entries


# --- Section splitting -------------------------------------------------------


def _build_section(name: str, body: list[SyntaxTreeNode]) -> ParsedSection:
    """Build a ParsedSection from a heading name and its body nodes."""
    desc_children = _extract_description_children(body)
    desc = render_inline_text(desc_children) if desc_children else ""
    desc_html = render_inline_html(desc_children) if desc_children else ""
    content_nodes = body[1:] if desc_children else body
    entries = _parse_section_entries(content_nodes)
    entry_count = len(entries) + sum(len(e["also_see"]) for e in entries)
    return ParsedSection(
        name=name,
        slug=slugify(name),
        description=desc,
        description_html=desc_html,
        entries=entries,
        entry_count=entry_count,
    )


def _is_bold_marker(node: SyntaxTreeNode) -> str | None:
    """Detect a bold-only paragraph used as a group marker.

    Pattern: a paragraph whose only content is **Group Name** (possibly
    surrounded by empty text nodes in the AST).
    Returns the group name text, or None if not a group marker.
    """
    if node.type != "paragraph":
        return None
    for child in node.children:
        if child.type != "inline":
            continue
        # Filter out empty text nodes that markdown-it inserts around strong
        meaningful = [c for c in child.children if not (c.type == "text" and c.content == "")]
        if len(meaningful) == 1 and meaningful[0].type == "strong":
            return render_inline_text(meaningful[0].children)
    return None


def _parse_grouped_sections(
    nodes: list[SyntaxTreeNode],
) -> list[ParsedGroup]:
    """Parse nodes into groups of categories using bold markers as group boundaries.

    Bold-only paragraphs (**Group Name**) delimit groups. H3 headings under each
    bold marker become categories within that group. Categories appearing before
    any bold marker go into an "Other" group.
    """
    groups: list[ParsedGroup] = []
    current_group_name: str | None = None
    current_group_cats: list[ParsedSection] = []
    current_cat_name: str | None = None
    current_cat_body: list[SyntaxTreeNode] = []

    def flush_cat() -> None:
        nonlocal current_cat_name
        if current_cat_name is None:
            return
        current_group_cats.append(_build_section(current_cat_name, current_cat_body))
        current_cat_name = None

    def flush_group() -> None:
        nonlocal current_group_name, current_group_cats
        if current_group_cats:
            name = current_group_name or "Other"
            groups.append(
                ParsedGroup(
                    name=name,
                    slug=slugify(name),
                    categories=list(current_group_cats),
                )
            )
        current_group_name = None
        current_group_cats = []

    for node in nodes:
        bold_name = _is_bold_marker(node)
        if bold_name is not None:
            flush_cat()
            flush_group()
            current_group_name = bold_name
            current_cat_body = []
        elif node.type == "heading" and node.tag in ("h2", "h3"):
            flush_cat()
            current_cat_name = _heading_text(node)
            current_cat_body = []
        elif current_cat_name is not None:
            current_cat_body.append(node)

    flush_cat()
    flush_group()
    return groups


_SPONSOR_SEP_RE = re.compile(r"^\s*[:\-\u2013\u2014]\s*")


def _find_link_deep(node: SyntaxTreeNode) -> SyntaxTreeNode | None:
    """Find the first link anywhere in the subtree (including nested in strong/em)."""
    for child in node.children:
        if child.type == "link":
            return child
        found = _find_link_deep(child)
        if found:
            return found
    return None


def _parse_sponsor_item(inline: SyntaxTreeNode) -> ParsedSponsor | None:
    """Parse `**[name](url)**: description` (or `[name](url) - description`)."""
    for split_idx, child in enumerate(inline.children):
        link = child if child.type == "link" else _find_link_deep(child)
        if link is None:
            continue
        desc_html = render_inline_html(inline.children[split_idx + 1 :])
        return ParsedSponsor(
            name=render_inline_text(link.children),
            url=_href(link),
            description=_SPONSOR_SEP_RE.sub("", desc_html),
        )
    return None


def parse_sponsors(text: str) -> list[ParsedSponsor]:
    """Parse the `Sponsors` section of README.md into a list of sponsors.

    Expects bullets in the form `**[name](url)**: description`.
    Returns [] if no Sponsors section exists.
    """
    md = MarkdownIt("commonmark")
    tokens = md.parse(text)
    root = SyntaxTreeNode(tokens)
    children = root.children

    start_idx = None
    end_idx = len(children)
    start_level = None
    for i, node in enumerate(children):
        level = _heading_level(node)
        if level is None:
            continue
        title = _heading_text(node).strip().lower()
        if start_idx is None and title == "sponsors":
            start_idx = i + 1
            start_level = level
        elif start_idx is not None and start_level is not None and level <= start_level:
            end_idx = i
            break
    if start_idx is None:
        return []

    sponsors: list[ParsedSponsor] = []
    for node in children[start_idx:end_idx]:
        if node.type != "bullet_list":
            continue
        for list_item in node.children:
            if list_item.type != "list_item":
                continue
            inline = _find_inline(list_item)
            if inline is None:
                continue
            sponsor = _parse_sponsor_item(inline)
            if sponsor:
                sponsors.append(sponsor)
    return sponsors


def parse_readme(text: str) -> list[ParsedGroup]:
    """Parse README.md text into grouped categories.

    Returns a list of ParsedGroup dicts containing nested categories.
    Content between the Projects heading and Resources or Contributing is parsed
    as categories grouped by bold markers (**Group Name**).
    """
    md = MarkdownIt("commonmark")
    tokens = md.parse(text)
    root = SyntaxTreeNode(tokens)
    children = root.children

    # Find Projects and section boundaries in one pass.
    projects_idx = None
    cat_end_idx = None
    for i, node in enumerate(children):
        if _heading_level(node) in (1, 2):
            text_content = _heading_text(node)
            if projects_idx is None and text_content == "Projects":
                projects_idx = i
            elif cat_end_idx is None and text_content in ("Resources", "Contributing"):
                cat_end_idx = i
    if projects_idx is None:
        return []

    cat_nodes = children[projects_idx + 1 : cat_end_idx or len(children)]
    return _parse_grouped_sections(cat_nodes)



================================================
FILE: website/data/pypi_name_overrides.json
================================================
{
  "autobahn-python": { "package": "autobahn", "reason": null },
  "azure-sdk-for-python": { "package": null, "reason": "monorepo umbrella; ships as many azure-* packages, no single package represents it", "badge": "Multiple on PyPI" },
  "betterleaks": { "package": null, "reason": "not published on PyPI" },
  "cloud-init": { "package": null, "reason": "installed via distro images, not pip" },
  "concurrent-futures": { "package": null, "reason": "stdlib module" },
  "conda": { "package": null, "reason": "installed via Miniforge or Anaconda installers; PyPI conda is a stale 2017 upload" },
  "cpython": { "package": null, "reason": "not pip-installable; the cpython PyPI name was squatted" },
  "devpi": { "package": "devpi-server", "reason": "devpi is a deprecated metapackage; the server package carries real usage" },
  "difflib": { "package": null, "reason": "stdlib module" },
  "django-ai-plugins": { "package": null, "reason": "GitHub-only so far; young project, remap if it publishes" },
  "django-db-models": { "package": null, "reason": "part of Django, not a package" },
  "django-rest-framework": { "package": "djangorestframework", "reason": "django-rest-framework is a dead alias package" },
  "django-rules": { "package": "rules", "reason": "PyPI django-rules is an abandoned unrelated fork; dfunckt's project publishes as rules" },
  "fasthtml": { "package": "python-fasthtml", "reason": null },
  "geodjango": { "package": null, "reason": "part of Django (django.contrib.gis), not a package" },
  "google-cloud-python": { "package": null, "reason": "monorepo umbrella; ships as many google-cloud-* packages", "badge": "Multiple on PyPI" },
  "graphify": { "package": "graphifyy", "reason": null },
  "httpx-url": { "package": null, "reason": "class in the httpx package, not a package" },
  "jinja": { "package": "jinja2", "reason": "PyPI jinja is Jinja1; current releases publish as jinja2" },
  "mem0": { "package": "mem0ai", "reason": null },
  "micropython": { "package": null, "reason": "interpreter distributed as firmware builds, not pip" },
  "mimetypes": { "package": null, "reason": "stdlib module" },
  "mise": { "package": null, "reason": "not published on PyPI; PyPI mise is an unrelated package" },
  "odoo": { "package": null, "reason": "self-hosted suite installed from odoo.com, not pip" },
  "pangu-py": { "package": "pangu", "reason": null },
  "playwright-python": { "package": "playwright", "reason": null },
  "pyenv": { "package": null, "reason": "installed via git/homebrew; PyPI pyenv is a defunct shim" },
  "pyodide": { "package": null, "reason": "runs in the browser from a CDN or npm; PyPI pyodide is a 0.0.2 placeholder from 2021" },
  "pypy": { "package": null, "reason": "interpreter distributed via pypy.org, not pip" },
  "python-patterns": { "package": null, "reason": "reference repo, not a package; PyPI name held by unrelated 2012 project" },
  "pytorch": { "package": "torch", "reason": "PyPI pytorch is a squatter; real package is torch" },
  "renpy": { "package": null, "reason": "distributed via renpy.org; PyPI name was squatted, now 404" },
  "scientific-agent-skills": { "package": null, "reason": "agent skills repo, not a package" },
  "sentry-skills": { "package": null, "reason": "agent skills repo, not a package" },
  "social-engineer-toolkit": { "package": null, "reason": "GitHub-only, installed from source" },
  "sqlite3": { "package": null, "reason": "stdlib module" },
  "strawberry": { "package": "strawberry-graphql", "reason": "PyPI strawberry is an unrelated bookmarking service" },
  "strawberry-django": { "package": "strawberry-graphql-django", "reason": null },
  "thealgorithms": { "package": null, "reason": "educational monorepo, not a package" },
  "tkinter": { "package": null, "reason": "stdlib module" },
  "tomllib": { "package": null, "reason": "stdlib module" },
  "trailofbits-skills": { "package": null, "reason": "agent skills repo, not a package" },
  "unittest-mock": { "package": null, "reason": "stdlib module" },
  "uv-audit": { "package": null, "reason": "part of uv (the `uv audit` subcommand); PyPI uv-audit is an unrelated third-party tool by rocshers" },
  "winpython": { "package": null, "reason": "distribution with its own installer; PyPI name is a 2012 relic" },
  "wshobson-agents": { "package": null, "reason": "agent skills repo, not a package" },
  "zoneinfo": { "package": null, "reason": "stdlib module" }
}



================================================
FILE: website/static/main.js
================================================
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

function getScrollBehavior() {
  return reducedMotion.matches ? "auto" : "smooth";
}

const table = document.querySelector(".table");
// Category pages list rows in editorial (README) order until a column is sorted
const defaultSort =
  table && table.dataset.defaultSort === "editorial"
    ? { col: "editorial", order: "asc" }
    : { col: "downloads", order: "desc" };
let activeSort = defaultSort;
const searchInput = document.querySelector(".search");
// The full placeholder is cut off on phones
if (searchInput && window.matchMedia("(max-width: 680px)").matches) {
  searchInput.placeholder = searchInput.dataset.shortPlaceholder;
}
const noResults = document.querySelector(".no-results");
const rows = document.querySelectorAll(".table tbody tr.row");
const tbody = document.querySelector(".table tbody");
const groupRows = document.querySelectorAll(".table tbody tr.group-row");

// Smooth scroll without hash in URL
document.querySelectorAll("[data-scroll-to]").forEach(function (link) {
  link.addEventListener("click", function (e) {
    const el = document.getElementById(link.dataset.scrollTo);
    if (!el) return;
    e.preventDefault();
    el.scrollIntoView({ behavior: getScrollBehavior() });
  });
});

// Land at #library-index without leaving the hash in the URL
if (window.location.hash === "#library-index") {
  const target = document.getElementById("library-index");
  if (target) {
    target.scrollIntoView();
  }
  history.replaceState(
    null,
    "",
    window.location.pathname + window.location.search,
  );
}

function relativeTime(isoStr) {
  const date = new Date(isoStr);
  const now = new Date();
  const diffMs = now - date;
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);
  if (diffHours < 1) return "just now";
  if (diffHours < 24)
    return diffHours === 1 ? "1 hour ago" : diffHours + " hours ago";
  if (diffDays === 1) return "yesterday";
  if (diffDays < 30) return diffDays + " days ago";
  const diffMonths = Math.floor(diffDays / 30);
  if (diffDays < 365)
    return diffMonths === 1 ? "1 month ago" : diffMonths + " months ago";
  const diffYears = Math.floor(diffDays / 365);
  return diffYears === 1 ? "1 year ago" : diffYears + " years ago";
}

document.querySelectorAll(".col-commit[data-commit]").forEach(function (td) {
  const time = td.querySelector("time");
  if (time) time.textContent = relativeTime(td.dataset.commit);
});

document
  .querySelectorAll(".expand-commit time[datetime]")
  .forEach(function (time) {
    time.textContent = relativeTime(time.getAttribute("datetime"));
  });

let currentGroupRow = null;
Array.prototype.forEach.call(tbody ? tbody.rows : [], function (tr) {
  if (tr.classList.contains("group-row")) currentGroupRow = tr;
  else if (tr.classList.contains("row")) tr._groupRow = currentGroupRow;
});

rows.forEach(function (row, i) {
  row._origIndex = i;
  let next = row.nextElementSibling;
  if (next && next.classList.contains("desc-row")) {
    row._descRow = next;
    next = next.nextElementSibling;
  }
  row._expandRow = next;
});

function setRowOpen(row, open) {
  row.classList.toggle("open", open);
  row.setAttribute("aria-expanded", String(open));
  // The homepage shows a row's description only while the row is open
  if (isIndexDocument && row._descRow) row._descRow.hidden = !open;
}

function collapseAll() {
  if (!tbody) return;
  const openRows = tbody.querySelectorAll("tr.row.open");
  openRows.forEach(function (row) {
    setRowOpen(row, false);
  });
}

function applyFilters() {
  const query = searchInput ? searchInput.value.toLowerCase().trim() : "";
  const descRowsVisible = !isIndexDocument;
  let visibleCount = 0;

  collapseAll();

  // Number rows in their sorted DOM order, not the load order `rows` keeps
  const orderedRows = tbody ? tbody.querySelectorAll("tr.row") : rows;
  orderedRows.forEach(function (row) {
    let show = true;

    if (query) {
      if (!row._searchText) {
        let text = row.textContent.toLowerCase();
        if (row._descRow) {
          text += " " + row._descRow.textContent.toLowerCase();
        }
        if (row._expandRow) {
          text += " " + row._expandRow.textContent.toLowerCase();
        }
        row._searchText = text;
      }
      show = row._searchText.includes(query);
    }

    if (row.hidden !== !show) row.hidden = !show;
    if (row._descRow) {
      const descHidden = !show || !descRowsVisible;
      if (row._descRow.hidden !== descHidden) {
        row._descRow.hidden = descHidden;
      }
    }

    if (show) {
      visibleCount++;
      const numCell = row.cells[0];
      if (numCell.textContent !== String(visibleCount)) {
        numCell.textContent = String(visibleCount);
      }
    }
  });

  groupRows.forEach(function (groupRow) {
    groupRow.hidden = true;
  });
  if (activeSort.col === "editorial") {
    rows.forEach(function (row) {
      if (!row.hidden && row._groupRow) row._groupRow.hidden = false;
    });
  }

  if (noResults) noResults.hidden = visibleCount > 0;

  updateURL();
}

const isIndexDocument =
  location.pathname === "/" || location.pathname === "/index.html";

function buildQueryString() {
  const params = new URLSearchParams();
  const query = searchInput ? searchInput.value.trim() : "";
  if (query) params.set("q", query);
  if (activeSort.col !== defaultSort.col || activeSort.order !== defaultSort.order) {
    params.set("sort", activeSort.col);
    params.set("order", activeSort.order);
  }
  const qs = params.toString();
  return qs ? "?" + qs : "";
}

function updateURL() {
  if (!isIndexDocument) return;
  history.replaceState(null, "", "/" + buildQueryString());
}

function getSortValue(row, col) {
  // +1 keeps the first row above the "no value" cutoff in sortRows
  if (col === "editorial") return row._origIndex + 1;
  if (col === "name") {
    return row.querySelector(".col-name a").textContent.trim().toLowerCase();
  }
  if (col === "stars") {
    const text = row
      .querySelector(".col-stars")
      .textContent.trim()
      .replace(/,/g, "");
    const num = parseInt(text, 10);
    return isNaN(num) ? -1 : num;
  }
  if (col === "downloads") {
    const text = row
      .querySelector(".col-downloads")
      .textContent.trim()
      .replace(/,/g, "");
    const num = parseInt(text, 10);
    return isNaN(num) ? -1 : num;
  }
  if (col === "commit-time") {
    const attr = row.querySelector(".col-commit").getAttribute("data-commit");
    return attr ? new Date(attr).getTime() : 0;
  }
  return 0;
}

function sortRows() {
  if (!tbody) return;

  const arr = Array.prototype.slice.call(rows);
  const col = activeSort.col;
  const order = activeSort.order;

  // Cache sort values once to avoid DOM queries per comparison
  arr.forEach(function (row) {
    row._sortVal = getSortValue(row, col);
  });

  arr.sort(function (a, b) {
    const aVal = a._sortVal;
    const bVal = b._sortVal;
    if (col === "name") {
      const cmp = aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
      if (cmp === 0) return a._origIndex - b._origIndex;
      return order === "desc" ? -cmp : cmp;
    }
    if (aVal <= 0 && bVal <= 0) return a._origIndex - b._origIndex;
    if (aVal <= 0) return 1;
    if (bVal <= 0) return -1;
    const cmp = aVal - bVal;
    if (cmp === 0) return a._origIndex - b._origIndex;
    return order === "desc" ? -cmp : cmp;
  });

  const frag = document.createDocumentFragment();
  let lastGroupRow = null;
  arr.forEach(function (row) {
    if (col === "editorial" && row._groupRow && row._groupRow !== lastGroupRow) {
      frag.appendChild(row._groupRow);
      lastGroupRow = row._groupRow;
    }
    frag.appendChild(row);
    if (row._descRow) frag.appendChild(row._descRow);
    if (row._expandRow) frag.appendChild(row._expandRow);
  });
  tbody.appendChild(frag);
  applyFilters();
}

const sortHeaders = document.querySelectorAll("th[data-sort]");

function updateSortIndicators() {
  if (table) table.classList.toggle("sorted", activeSort.col !== "editorial");
  sortHeaders.forEach(function (th) {
    th.classList.remove("sort-asc", "sort-desc");
    if (th.dataset.sort === activeSort.col) {
      th.classList.add("sort-" + activeSort.order);
      th.setAttribute(
        "aria-sort",
        activeSort.order === "asc" ? "ascending" : "descending",
      );
    } else {
      th.removeAttribute("aria-sort");
    }
  });
}

// Expand/collapse: event delegation on tbody
if (tbody) {
  tbody.addEventListener("click", function (e) {
    // Don't toggle if clicking a link
    if (e.target.closest("a")) return;

    let row = e.target.closest("tr.row");
    if (!row) {
      const descRow = e.target.closest("tr.desc-row");
      if (descRow) row = descRow.previousElementSibling;
    }
    if (!row) return;

    setRowOpen(row, !row.classList.contains("open"));
  });

  // Keyboard: Enter or Space on focused .row toggles expand
  tbody.addEventListener("keydown", function (e) {
    if (e.key !== "Enter" && e.key !== " ") return;
    if (e.target.closest("a")) return;
    const row = e.target.closest("tr.row");
    if (!row) return;
    e.preventDefault();
    row.click();
  });
}

const noResultsClear = document.querySelector(".no-results-clear");
if (noResultsClear) {
  noResultsClear.addEventListener("click", function () {
    if (!isIndexDocument) {
      window.location.href = "/";
      return;
    }
    if (searchInput) searchInput.value = "";
    applyFilters();
  });
}

sortHeaders.forEach(function (th) {
  th.addEventListener("click", function () {
    const col = th.dataset.sort;
    const defaultOrder = col === "name" ? "asc" : "desc";
    const altOrder = defaultOrder === "asc" ? "desc" : "asc";
    if (activeSort.col === col) {
      if (activeSort.order === defaultOrder)
        activeSort = { col: col, order: altOrder };
      else activeSort = defaultSort;
    } else {
      activeSort = { col: col, order: defaultOrder };
    }
    sortRows();
    updateSortIndicators();
  });
});

function openEntryRow(row) {
  if (row.hidden && searchInput) {
    searchInput.value = "";
    applyFilters();
  }
  setRowOpen(row, true);
}

// Group headings are hidden while sorted flat or filtered out by search, so a link to one must restore them first
document.addEventListener("click", function (e) {
  const link = e.target.closest('a[href*="#"]');
  if (!link || link.pathname !== location.pathname) return;
  const target = document.getElementById(decodeURIComponent(link.hash.slice(1)));
  if (target && target.matches("tr.row")) {
    openEntryRow(target);
    return;
  }
  const groupRow = target ? target.closest(".group-row") : null;
  if (!groupRow) return;
  if (activeSort.col !== "editorial") {
    activeSort = defaultSort;
    sortRows();
    updateSortIndicators();
  }
  if (groupRow.hidden && searchInput) {
    searchInput.value = "";
    applyFilters();
  }
});

// Mailto clicks leave no page view, so the sponsor funnel needs its own event
document.addEventListener("click", function (e) {
  const link = e.target.closest('a[href^="mailto:sponsorship@"]');
  if (!link || typeof gtag !== "function") return;
  gtag("event", "sponsor_contact", { tier: link.dataset.tier });
});

if (location.hash) {
  const linkedRow = document.getElementById(decodeURIComponent(location.hash.slice(1)));
  if (linkedRow && linkedRow.matches("tr.row")) openEntryRow(linkedRow);
}

if (searchInput) {
  let searchTimer;
  searchInput.addEventListener("input", function () {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(applyFilters, 150);
  });

  document.addEventListener("keydown", function (e) {
    if (
      e.key === "/" &&
      !["INPUT", "TEXTAREA", "SELECT"].includes(
        document.activeElement.tagName,
      ) &&
      !e.ctrlKey &&
      !e.metaKey
    ) {
      e.preventDefault();
      searchInput.focus();
    }
    if (e.key === "Escape" && document.activeElement === searchInput) {
      searchInput.value = "";
      applyFilters();
      searchInput.blur();
    }
  });
}

const backToTop = document.querySelector(".back-to-top");
const resultsSection = document.querySelector("#library-index");
const tableWrap = document.querySelector(".table-wrap");
const stickyHeaderCell = backToTop ? backToTop.closest("th") : null;

function updateBackToTopVisibility() {
  if (!backToTop || !tableWrap || !stickyHeaderCell) return;

  const tableRect = tableWrap.getBoundingClientRect();
  const headRect = stickyHeaderCell.getBoundingClientRect();
  const hasPassedHeader = tableRect.top <= 0 && headRect.bottom > 0;

  backToTop.classList.toggle("visible", hasPassedHeader);
}

if (backToTop) {
  let scrollTicking = false;
  window.addEventListener("scroll", function () {
    if (!scrollTicking) {
      requestAnimationFrame(function () {
        updateBackToTopVisibility();
        scrollTicking = false;
      });
      scrollTicking = true;
    }
  });

  window.addEventListener("resize", updateBackToTopVisibility);

  backToTop.addEventListener("click", function () {
    const target = searchInput || resultsSection;
    if (!target) return;
    target.scrollIntoView({ behavior: getScrollBehavior(), block: "center" });
    if (searchInput) searchInput.focus();
  });

  updateBackToTopVisibility();
}

(function () {
  const params = new URLSearchParams(location.search);
  const q = params.get("q");
  const sort = params.get("sort");
  const order = params.get("order");
  if (q && searchInput) searchInput.value = q;
  if (
    (sort === "name" ||
      sort === "stars" ||
      sort === "downloads" ||
      sort === "commit-time") &&
    (order === "desc" || order === "asc")
  ) {
    activeSort = { col: sort, order: order };
  }
  if (q || sort) {
    sortRows();
  }
  updateSortIndicators();
})();



================================================
FILE: website/static/style.css
================================================
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

:root {
  color-scheme: light;
  --font-display: "Cormorant Garamond", Georgia, serif;
  --font-body: "Manrope", "Avenir Next", "Segoe UI", sans-serif;

  --shell-max: 84rem;
  --shell-pad: clamp(1.25rem, 3vw, 2.5rem);

  --bg-page: oklch(96.8% 0.018 80);
  --bg-page-top: oklch(95.2% 0.018 78);
  --bg-page-end: oklch(98.4% 0.01 80);
  --bg-paper: oklch(98.6% 0.01 80);
  --bg-paper-strong: oklch(95.7% 0.016 76);
  --ink: oklch(22% 0.02 55);
  --ink-soft: oklch(38% 0.018 55);
  --ink-muted: oklch(52% 0.02 55);
  --line: oklch(83% 0.02 70);
  --line-strong: oklch(64% 0.035 62);
  --accent: oklch(58% 0.16 45);
  --accent-deep: oklch(44% 0.15 42);
  --accent-soft: oklch(92% 0.045 55);
  --accent-underline: oklch(58% 0.16 45 / 0.4);
  --highlight: oklch(87% 0.08 78);

  --hero-ink: oklch(15% 0.02 40);
  --hero-text: oklch(97% 0.012 85);
  --hero-muted: oklch(88% 0.02 82);
  --hero-line: oklch(100% 0 0 / 0.16);
  --hero-kicker: oklch(82% 0.04 72);
  --hero-proof: oklch(75% 0.02 72);
  --hero-bg-start: oklch(14% 0.03 32);
  --hero-bg-mid: oklch(19% 0.035 35);
  --hero-bg-end: oklch(28% 0.05 42);
  --hero-btn-start: oklch(83% 0.08 72);
  --hero-btn-end: oklch(73% 0.14 58);

  --row-hover: oklch(96.2% 0.02 76);
  --row-focus: oklch(95.7% 0.026 68);
  --row-open: oklch(95.8% 0.028 75);
  --thead-bg: oklch(98.2% 0.012 80 / 0.97);

  --search-inset: oklch(100% 0 0 / 0.75);
  --search-shadow: oklch(18% 0.03 45 / 0.24);
  --search-focus-ring: oklch(61% 0.14 48 / 0.45);
  --search-focus-shadow: oklch(34% 0.08 42 / 0.28);

  --tag-hover-border: oklch(71% 0.09 62 / 0.45);
  --tag-active-start: oklch(82% 0.08 75);
  --tag-active-end: oklch(74% 0.11 58);

  --cta-bg: oklch(94% 0.025 72);
  --sponsor-bg: oklch(91% 0.04 68);

  --text-xs: 0.8rem;
  --text-sm: 0.95rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;

  --display-sm: clamp(1.75rem, 2.8vw, 2.25rem);
  --display-md: clamp(2.25rem, 4.2vw, 3.3rem);
  --display-lg: clamp(3.6rem, 9vw, 7rem);

  --footer-bg: oklch(16% 0.025 35);
  --footer-text: oklch(72% 0.02 75);
  --footer-link: oklch(82% 0.02 75);
  --footer-link-hover: oklch(95% 0.01 80);

  --footer-sep: oklch(55% 0.02 55);
}

html {
  font-size: 100%;
  scroll-behavior: smooth;
}

body {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: var(--font-body);
  line-height: 1.6;
  color: var(--ink);
  background:
    radial-gradient(circle at top left, oklch(100% 0 0 / 0.72), transparent 28rem),
    linear-gradient(180deg, var(--bg-page-top), var(--bg-page) 24rem, var(--bg-page-end));
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

main {
  display: flex;
  flex-direction: column;
}

a {
  color: inherit;
  text-decoration: none;
}

button,
input {
  font: inherit;
}

img,
svg {
  display: block;
  max-width: 100%;
}

kbd {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.8em;
  padding: 0.08rem 0.38rem;
  border: 1px solid var(--line);
  border-bottom-width: 2px;
  border-radius: 999px;
  background: var(--bg-paper);
  font-size: 0.85em;
  line-height: 1.2;
}

.section-shell {
  width: min(100%, calc(var(--shell-max) + (var(--shell-pad) * 2)));
  margin: 0 auto;
  padding-inline: var(--shell-pad);
}

.skip-link {
  position: absolute;
  left: -9999px;
  top: 0;
  z-index: 300;
  padding: 0.75rem 1rem;
  color: var(--hero-text);
  background: var(--hero-ink);
  font-size: var(--text-sm);
  font-weight: 700;
}

.skip-link:focus {
  left: 1rem;
  top: 1rem;
}

.hero {
  position: relative;
  width: 100%;
  overflow: clip;
  background:
    radial-gradient(circle at 18% 18%, oklch(55% 0.14 45 / 0.34), transparent 22rem),
    radial-gradient(circle at 78% 32%, oklch(62% 0.17 70 / 0.17), transparent 24rem),
    linear-gradient(140deg, var(--hero-bg-start) 0%, var(--hero-bg-mid) 52%, var(--hero-bg-end) 100%);
  color: var(--hero-text);
}

.hero::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, oklch(100% 0 0 / 0.03) 1px, transparent 1px),
    linear-gradient(oklch(100% 0 0 / 0.03) 1px, transparent 1px);
  background-size: 7rem 7rem;
  mask-image: linear-gradient(180deg, oklch(0% 0 0 / 0.72), transparent 88%);
  pointer-events: none;
}

.hero-noise {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.hero-noise {
  opacity: 0.1;
  background-image:
    radial-gradient(circle at 20% 20%, oklch(100% 0 0 / 0.65) 0.02rem, transparent 0.04rem),
    radial-gradient(circle at 80% 30%, oklch(100% 0 0 / 0.55) 0.03rem, transparent 0.05rem);
  background-size: 4rem 4rem, 5rem 5rem;
}

.hero-shell {
  position: relative;
  z-index: 1;
  width: min(100%, calc(var(--shell-max) + (var(--shell-pad) * 2)));
  margin: 0 auto;
  padding: 1.25rem var(--shell-pad);
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.hero-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.hero-brand-mini {
  font-size: var(--text-xs);
  font-weight: 800;
  letter-spacing: 0.04em;
  color: var(--hero-muted);
}

.hero-topbar-link:hover {
  color: var(--hero-text);
}

.hero-sub a:hover {
  color: var(--hero-text);
  text-decoration-color: oklch(100% 0 0 / 0.6);
}

.hero-topbar-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
}

.hero-topbar-link {
  padding: 0.45rem 0.8rem;
  border: 1px solid var(--hero-line);
  border-radius: 999px;
  color: var(--hero-muted);
  font-size: var(--text-xs);
  font-weight: 700;
  letter-spacing: 0.02em;
  transition:
    color 180ms ease,
    border-color 180ms ease,
    background-color 180ms ease,
    transform 180ms ease;
}

.hero-topbar-link-strong,
.hero-topbar-link:hover {
  border-color: oklch(100% 0 0 / 0.28);
  background: oklch(100% 0 0 / 0.06);
}

.hero-topbar-link:active,
.hero-action:active,
.tag:active {
  transform: translateY(1px);
}

.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  align-items: center;
  gap: 0;
  flex: 1;
}

.hero-copy {
  width: 100%;
  max-width: none;
}

.hero-kicker,
.section-label {
  margin-bottom: 1.5rem;
  font-size: var(--text-sm);
  font-weight: 800;
  letter-spacing: 0.04em;
}

.hero-kicker {
  color: var(--hero-kicker);
}

.hero h1 {
  font-family: var(--font-display);
  font-size: clamp(4.5rem, 11vw, 8.5rem);
  line-height: 0.9;
  font-weight: 600;
  letter-spacing: -0.03em;
  text-wrap: balance;
}

.hero-sub {
  margin-top: 2rem;
  color: var(--hero-muted);
  font-size: var(--text-xl);
  text-wrap: pretty;
}

.hero-sub a {
  color: var(--hero-text);
  text-decoration: underline;
  text-decoration-color: oklch(100% 0 0 / 0.25);
  text-underline-offset: 0.2em;
}

.hero-actions,
.final-cta-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
}

.hero-actions {
  margin-top: 1.75rem;
}

.hero-proof {
  margin-top: 0.5rem;
  color: var(--hero-proof);
  font-size: var(--text-sm);
  letter-spacing: 0.02em;
}

/* Keeps each stat whole when the line wraps */
.proof-stat {
  white-space: nowrap;
}

.hero-proof a {
  color: var(--hero-text);
  text-decoration: underline;
  text-decoration-color: oklch(100% 0 0 / 0.25);
  text-underline-offset: 0.2em;
}

.hero-proof a:hover {
  text-decoration-color: oklch(100% 0 0 / 0.6);
}

.hero-category-nav {
  padding-top: 1.35rem;
  border-top: 1px solid var(--hero-line);
}

.hero-category-details {
  display: grid;
  grid-template-columns: minmax(10rem, 14rem) minmax(0, 1fr);
  gap: clamp(1.5rem, 4vw, 3rem);
  align-items: start;
}

.hero-category-meta {
  display: block;
  cursor: pointer;
}

.hero-category-meta::-webkit-details-marker {
  display: none;
}

.hero-category-meta h2 {
  color: var(--hero-kicker);
  font-size: var(--text-sm);
  font-weight: 800;
  letter-spacing: 0.04em;
}

.hero-category-meta h2::after {
  content: " ↓";
}

.hero-category-details[open] .hero-category-meta h2::after {
  content: " ↑";
}

.hero-category-links {
  list-style: none;
  columns: 13rem;
  column-gap: clamp(1.25rem, 3vw, 2.5rem);
}

.hero-category-links li {
  break-inside: avoid;
  padding-bottom: 0.28rem;
}

.hero-category-link {
  color: var(--hero-muted);
  font-size: var(--text-xs);
  font-weight: 700;
  line-height: 1.35;
  text-decoration: underline;
  text-decoration-color: transparent;
  text-underline-offset: 0.18em;
  transition:
    color 180ms ease,
    text-decoration-color 180ms ease;
}

.hero-category-link:hover {
  color: var(--hero-text);
  text-decoration-color: oklch(100% 0 0 / 0.42);
}

.hero-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 3rem;
  padding: 0.85rem 1.25rem;
  border-radius: 999px;
  border: 1px solid transparent;
  font-size: var(--text-sm);
  font-weight: 700;
  letter-spacing: 0.01em;
  transition:
    transform 180ms ease,
    color 180ms ease,
    background-color 180ms ease,
    border-color 180ms ease,
    box-shadow 180ms ease;
}

.hero-action-primary {
  color: var(--hero-ink);
  background: linear-gradient(135deg, var(--hero-btn-start), var(--hero-btn-end));
  box-shadow: 0 1.2rem 2.5rem -1.5rem oklch(0% 0 0 / 0.65);
}

.hero-action-primary:hover {
  box-shadow: 0 1.5rem 2.7rem -1.4rem oklch(0% 0 0 / 0.8);
}

.hero-action-secondary {
  color: var(--hero-text);
  border-color: var(--hero-line);
  background: oklch(100% 0 0 / 0.04);
}

.hero-action-secondary:hover {
  background: oklch(100% 0 0 / 0.08);
  border-color: oklch(100% 0 0 / 0.28);
}

.hero-action:focus-visible,
.hero-brand-mini:focus-visible,
.hero-topbar-link:focus-visible,
.hero-category-link:focus-visible,
.hero-category-meta:focus-visible,
.search:focus-visible,
.tag:focus-visible,
.jump-link:focus-visible,
.back-to-top:focus-visible,
.no-results-clear:focus-visible,
.table a:focus-visible,
.footer a:focus-visible,
.sort-btn:focus-visible,
.hero-sub a:focus-visible,
.hero-proof a:focus-visible,
.category-breadcrumb a:focus-visible,
.category-subtitle a:focus-visible,
.category-intro a:focus-visible,
.guide-body a:focus-visible,
.group-lead a:focus-visible,
.sponsor-become:focus-visible,
.sponsor-link:focus-visible,
.sponsor-desc a:focus-visible,
.sponsorship-body a:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 3px;
}

.category-hero {
  position: relative;
  overflow: clip;
  background: linear-gradient(140deg, var(--hero-bg-start) 0%, var(--hero-bg-mid) 58%, var(--hero-bg-end) 100%);
  color: var(--hero-text);
}

.category-hero-shell {
  position: relative;
  z-index: 1;
  width: min(100%, calc(var(--shell-max) + (var(--shell-pad) * 2)));
  margin: 0 auto;
  /* The bottom is a little smaller because the jump links' text sits inside its line box */
  padding: 1.25rem var(--shell-pad) 1.1rem;
  display: grid;
  gap: clamp(2rem, 5vw, 3rem);
}

.category-hero h1 {
  font-family: var(--font-display);
  font-size: var(--display-lg);
  line-height: 0.9;
  font-weight: 600;
  text-wrap: balance;
}

.category-breadcrumb {
  margin: 0 0 1rem;
  color: var(--hero-muted);
  font-size: var(--text-lg);
}

.category-breadcrumb a {
  color: var(--hero-text);
  text-decoration: underline;
  text-decoration-color: oklch(100% 0 0 / 0.32);
  text-underline-offset: 0.2em;
}

.category-breadcrumb a:hover {
  text-decoration-color: oklch(100% 0 0 / 0.7);
}

.category-subtitle {
  /* Cormorant descenders hang ~0.28em below the h1's 0.9 line box, so the gap scales with the h1. */
  margin-top: max(1.1rem, var(--display-lg) * 0.3);
  color: var(--hero-muted);
  font-size: var(--text-xl);
  text-wrap: pretty;
}

.category-subtitle a,
.category-intro a,
.guide-body a,
.jump-link {
  color: var(--hero-text);
  text-decoration: underline;
  text-decoration-color: oklch(100% 0 0 / 0.32);
  text-underline-offset: 0.2em;
}

.category-subtitle a:hover,
.category-intro a:hover,
.guide-body a:hover,
.jump-link:hover {
  text-decoration-color: oklch(100% 0 0 / 0.7);
}

.category-intro {
  margin-top: 1.25rem;
  display: grid;
  gap: 0.9rem;
  color: var(--hero-muted);
  font-size: var(--text-xl);
  text-wrap: pretty;
}

.category-intro > p:first-child {
  color: var(--hero-text);
  font-size: var(--text-2xl);
  line-height: 1.45;
}

.category-intro ul {
  display: grid;
  gap: 0.35rem;
  padding-left: 1.25rem;
}

.category-intro code,
.guide-body code {
  font-family: ui-monospace, "SFMono-Regular", "Menlo", monospace;
  font-size: 0.9em;
  padding: 0.08rem 0.4rem;
  border-radius: 0.4rem;
  background: var(--hero-line);
  color: var(--hero-text);
}

.jump-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem 1.6rem;
  margin-top: 1.5rem;
}

.jump-link {
  font-size: var(--text-base);
  font-weight: 600;
}

/* The arrow marks an in-page jump; inline-block keeps it out of the underline */
.jump-link::after {
  content: "\2193";
  display: inline-block;
  margin-left: 0.3rem;
  color: var(--hero-kicker);
}

.guide-band {
  padding-block: calc(var(--shell-pad) * 1.2);
  background: linear-gradient(140deg, var(--hero-bg-start) 0%, var(--hero-bg-mid) 58%, var(--hero-bg-end) 100%);
  color: var(--hero-text);
}

.guide-section {
  display: grid;
  gap: 1.5rem;
}

.guide-section h2 {
  font-family: var(--font-display);
  font-size: var(--display-md);
  font-weight: 600;
  line-height: 0.94;
  letter-spacing: -0.03em;
}

.guide-body {
  display: grid;
  gap: 1rem;
  color: var(--hero-muted);
  font-size: var(--text-lg);
  line-height: 1.7;
  text-wrap: pretty;
}

.guide-body ul {
  display: grid;
  gap: 0.35rem;
  padding-left: 1.25rem;
}

.sponsor-band {
  --band-pad: clamp(2.5rem, 5.5vw, 4rem);
  /* The sponsor name's glyphs rise above its line box, so the top gap reads 1rem smaller than the padding */
  padding-block: var(--band-pad) calc(var(--band-pad) - 1rem);
  background: var(--sponsor-bg);
  border-bottom: 1px solid var(--line-strong);
}

.sponsor-shell {
  display: grid;
  grid-template-columns: minmax(0, 14rem) minmax(0, 1fr);
  gap: clamp(1.5rem, 5vw, 3.5rem);
  align-items: start;
}

.sponsor-meta {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sponsor-meta .section-label {
  margin-bottom: 0;
  font-size: var(--text-lg);
}

.sponsor-become {
  align-self: start;
  color: var(--ink-soft);
  font-size: var(--text-sm);
  font-weight: 700;
  letter-spacing: 0.01em;
  text-decoration: underline;
  text-decoration-color: var(--line-strong);
  text-underline-offset: 0.2em;
  transition:
    color 180ms ease,
    text-decoration-color 180ms ease;
}

.sponsor-become:hover {
  color: var(--accent-deep);
  text-decoration-color: var(--accent-underline);
}

.sponsor-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: clamp(1.5rem, 3vw, 2.25rem);
}

.sponsor {
  display: grid;
  gap: 0.65rem;
}

.sponsor-link {
  display: inline-flex;
  align-items: baseline;
  gap: 0.5rem;
  margin-block-start: -1rem;
  color: var(--ink);
  transition: color 180ms ease;
}

.sponsor-link:hover {
  color: var(--accent-deep);
}

.sponsor-name {
  font-family: var(--font-display);
  font-size: var(--display-md);
  font-weight: 600;
  line-height: 0.95;
  letter-spacing: -0.025em;
}

.sponsor-name::after {
  content: "\2197" / "";
  margin-left: 0.25em;
  font-family: var(--font-body);
  font-size: 0.45em;
  /* Centers the arrow on the name's cap height */
  vertical-align: 0.33em;
  color: var(--accent-deep);
}

.sponsor-desc {
  color: var(--ink-soft);
  font-size: var(--text-lg);
  line-height: 1.55;
}

.sponsor-desc a {
  color: var(--accent-deep);
  text-decoration: underline;
  text-decoration-color: var(--accent-underline);
  text-underline-offset: 0.18em;
}

.sponsor-desc a:hover {
  color: var(--accent);
}

.results-intro h2,
.final-cta h2 {
  font-family: var(--font-display);
  font-size: var(--display-md);
  font-weight: 600;
  line-height: 0.94;
  letter-spacing: -0.03em;
}

.results-section {
  padding-block: var(--shell-pad) 0;
  contain: layout style;
}

.results-intro {
  display: grid;
  grid-template-columns: minmax(0, 1fr) max-content;
  gap: 1.25rem;
  align-items: end;
  padding-bottom: 1.75rem;
}

.order-note {
  align-self: start;
  color: var(--ink-soft);
  font-size: var(--text-base);
}

.results-note {
  color: var(--ink-soft);
  font-size: var(--text-sm);
  justify-self: end;
}

/* Single-project pages drop the order note, so keep the note in the last column */
.results-note:only-child {
  grid-column: -2 / -1;
}

.controls {
  display: grid;
  gap: 0.85rem;
  /* Matches the visible gap above the section's first line of text */
  padding-bottom: calc(var(--shell-pad) + 0.5rem);
}

.search-wrap {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 1.15rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--ink-muted);
  pointer-events: none;
}

.search {
  width: 100%;
  min-height: 4.1rem;
  padding: 1rem 1.15rem 1rem 3.2rem;
  border: 1px solid transparent;
  border-radius: 999px;
  background: linear-gradient(180deg, oklch(100% 0 0 / 0.82), var(--bg-paper));
  color: var(--ink);
  font-size: var(--text-lg);
  box-shadow:
    inset 0 1px 0 var(--search-inset),
    0 1.4rem 2.6rem -2.1rem var(--search-shadow);
  transition:
    border-color 180ms ease,
    box-shadow 180ms ease,
    background-color 180ms ease;
}

.search::placeholder {
  color: var(--ink-muted);
}

.search:focus {
  border-color: var(--search-focus-ring);
  box-shadow:
    inset 0 1px 0 var(--search-inset),
    0 1.6rem 3rem -2rem var(--search-focus-shadow);
}

.table-wrap {
  width: 100%;
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
  scroll-margin-top: 1rem;
}

.table-wrap:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: -2px;
}

.table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: var(--text-sm);
}

.table thead th,
.table tbody td {
  padding-inline: 0.9rem;
}

.table thead th:first-child,
.table tbody td:first-child {
  padding-left: max(var(--shell-pad), calc(50vw - (var(--shell-max) / 2) + var(--shell-pad)));
}

.table thead th:last-child,
.table tbody td:last-child {
  padding-right: max(var(--shell-pad), calc(50vw - (var(--shell-max) / 2) + var(--shell-pad)));
}

.table thead th {
  position: sticky;
  top: 0;
  z-index: 12;
  padding-top: 1rem;
  padding-bottom: 0.95rem;
  text-align: left;
  color: var(--ink);
  font-size: var(--text-xs);
  font-weight: 800;
  letter-spacing: 0.03em;
  white-space: nowrap;
  border-bottom: 1px solid var(--line);
  background: var(--thead-bg);
}

.table tbody td {
  padding-top: 1rem;
  padding-bottom: 1rem;
  vertical-align: middle;
  border-bottom: 1px solid var(--line);
  transition:
    background-color 180ms ease,
    border-color 180ms ease;
}

.table tbody tr[hidden] {
  display: none;
}

.row {
  cursor: pointer;
  scroll-margin-top: 4.5rem;
}

.group-row th {
  padding-top: 2.25rem;
  padding-bottom: 0.85rem;
  padding-inline: max(var(--shell-pad), calc(50vw - (var(--shell-max) / 2) + var(--shell-pad)));
  text-align: left;
  border-bottom: 1px solid var(--line-strong);
  background: var(--bg-paper);
}

.group-row h2 {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  font-family: var(--font-display);
  font-size: var(--display-sm);
  font-weight: 600;
  line-height: 1;
  scroll-margin-top: 4.5rem;
}

.group-row h2 a {
  color: var(--ink);
}

.group-row h2 a:hover {
  color: var(--accent-deep);
  text-decoration: underline;
  text-decoration-color: var(--accent-underline);
  text-underline-offset: 0.2em;
}

/* main.js adds .sorted once a column sort flattens the groups */
.table:not(.sorted) .repeats-heading {
  display: none;
}

.group-lead {
  margin-top: 0.75rem;
  font-size: var(--text-lg);
  font-weight: 400;
  line-height: 1.55;
  color: var(--ink-soft);
  text-wrap: pretty;
}

.group-count {
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--ink-muted);
}

.row:not(.open):hover td {
  background: var(--row-hover);
}

.row:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: -2px;
}

.row:focus-visible td {
  background: var(--row-focus);
}

.row:has(+ .desc-row:not([hidden])) td {
  border-bottom-color: transparent;
  padding-bottom: 0.4rem;
}

.row.open td {
  padding-bottom: 0.35rem;
  background: var(--row-open);
  border-bottom-color: transparent;
}

.col-num {
  width: 3.5rem;
  color: var(--ink-muted);
  font-variant-numeric: tabular-nums;
}

.col-name {
  white-space: nowrap;
}

.mobile-cat {
  display: none;
}

.col-name > a {
  color: var(--ink);
  font-size: var(--text-lg);
  font-weight: 700;
  overflow-wrap: break-word;
  word-break: break-word;
}

.col-name > a:hover {
  color: var(--accent-deep);
  text-decoration: underline;
  text-decoration-color: var(--accent-underline);
  text-underline-offset: 0.2em;
}

th[data-sort] {
  cursor: pointer;
  user-select: none;
  transition: color 180ms ease;
}

th[data-sort]:hover {
  color: var(--accent-deep);
}

.sort-btn {
  background: none;
  border: 0;
  padding: 0;
  color: inherit;
  font: inherit;
  cursor: inherit;
}

th[data-sort]::after {
  content: " \2193";
  opacity: 0;
  transition: opacity 180ms ease;
}

th[data-sort="name"]::after {
  content: " \2191";
}

th[data-sort]:hover::after,
th[data-sort].sort-asc::after,
th[data-sort].sort-desc::after {
  opacity: 1;
}

th[data-sort].sort-desc::after {
  content: " \2193";
}

th[data-sort].sort-asc::after {
  content: " \2191";
}

.col-stars {
  width: 7rem;
  text-align: right;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
  color: var(--ink-soft);
}

.source-badge {
  display: inline-flex;
  align-items: center;
  min-height: 1.8rem;
  padding: 0.18rem 0.6rem;
  border-radius: 999px;
  background: var(--bg-paper-strong);
  color: var(--ink-soft);
  font-size: var(--text-xs);
  font-weight: 700;
  letter-spacing: 0.02em;
}

.col-downloads {
  width: 9.5rem;
  text-align: right;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
  color: var(--ink-soft);
}

.col-commit {
  width: 9rem;
  white-space: nowrap;
  color: var(--ink-muted);
}

.col-cat {
  white-space: nowrap;
}

.col-arrow {
  width: 3rem;
  text-align: center;
}

.arrow {
  display: inline-block;
  color: var(--accent-deep);
  font-size: 0.9rem;
  transition:
    transform 180ms ease,
    color 180ms ease;
}

.row:hover .arrow,
.row.open .arrow {
  color: var(--accent);
}

.row.open .arrow {
  transform: rotate(90deg);
}

.table .desc-row td {
  padding-top: 0;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--line);
  color: var(--ink-soft);
  font-size: var(--text-sm);
  line-height: 1.6;
  text-wrap: pretty;
  overflow-wrap: break-word;
  transition:
    background-color 180ms ease,
    border-color 180ms ease;
}

.row:not(.open) + .desc-row td {
  border-bottom: 1px solid var(--line);
}

.row + .desc-row {
  cursor: pointer;
}

.row:not(.open):hover td,
.row:not(.open):hover + .desc-row td {
  background: var(--row-hover);
}

.row.open + .desc-row td {
  padding-bottom: 0;
  background: var(--row-open);
  border-bottom-color: transparent;
}

.desc-text {
  max-width: none;
}

.desc-text a,
.group-lead a {
  color: var(--accent-deep);
}

.desc-text a:hover,
.group-lead a:hover {
  color: var(--accent);
  text-decoration: underline;
  text-decoration-color: var(--accent-underline);
  text-underline-offset: 0.2em;
}

.expand-row {
  display: none;
}

.row.open + .desc-row + .expand-row,
.row.open + .expand-row {
  display: table-row;
}

.table .expand-row td {
  padding-top: 0;
  background: var(--row-open);
  border-bottom: 1px solid var(--line);
}

.expand-content {
  font-size: var(--text-base);
  color: var(--ink-soft);
  line-height: 1.7;
  text-wrap: pretty;
  overflow-wrap: break-word;
  word-break: break-word;
  contain: layout style paint;
  animation: expand-in 220ms cubic-bezier(0.22, 1, 0.36, 1);
}

.expand-also-see a,
.expand-meta a,
.footer a {
  color: var(--accent-deep);
}

.expand-also-see a:hover,
.expand-meta a:hover {
  color: var(--accent);
  text-decoration: underline;
  text-decoration-color: var(--accent-underline);
  text-underline-offset: 0.2em;
}

.expand-also-see,
.expand-meta {
  margin-top: 0.3rem;
  font-size: var(--text-sm);
  color: var(--ink-muted);
}

.expand-meta a {
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: bottom;
}

.expand-sep {
  margin-inline: 0.25rem;
  color: var(--line-strong);
}

.expand-commit,
.expand-stars {
  display: none;
}

.tag {
  position: relative;
  border: 1px solid transparent;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent-deep);
  padding: 0.14rem 0.48rem;
  font-size: var(--text-xs);
  font-weight: 700;
  letter-spacing: 0.02em;
  cursor: pointer;
  transition:
    color 180ms ease,
    background-color 180ms ease,
    border-color 180ms ease,
    transform 180ms ease;
}

.tag + .tag {
  margin-left: 0.2rem;
}

.tag::after {
  content: "";
  position: absolute;
  inset: -0.5rem -0.25rem;
  min-height: 44px;
  min-width: 44px;
}

.tag:hover {
  background: var(--highlight);
  border-color: var(--tag-hover-border);
  color: var(--ink);
}

.tag.active {
  background: linear-gradient(135deg, var(--tag-active-start), var(--tag-active-end));
  color: var(--hero-ink);
}

.back-to-top {
  /* Grows the tap target past 24px without changing the header row height */
  padding-block: 0.5rem;
  margin-block: -0.5rem;
  border: 0;
  background: none;
  color: var(--accent-deep);
  font-size: var(--text-xs);
  font-weight: 800;
  letter-spacing: 0.03em;
  cursor: pointer;
  opacity: 0;
  pointer-events: none;
  transition:
    opacity 180ms ease,
    color 180ms ease;
}

.back-to-top.visible {
  opacity: 1;
  pointer-events: auto;
}

.back-to-top:hover {
  color: var(--accent);
}

.no-results {
  padding: 2.4rem var(--shell-pad);
  text-align: center;
  color: var(--ink-muted);
  font-size: var(--text-lg);
}

.no-results-hint {
  margin-top: 0.5rem;
  font-size: var(--text-sm);
}

.no-results-clear {
  background: none;
  border: none;
  color: var(--accent-deep);
  font: inherit;
  cursor: pointer;
  text-decoration: underline;
  text-decoration-color: var(--accent-underline);
  text-underline-offset: 0.2em;
}

.no-results-clear:hover {
  color: var(--accent);
}

.sponsorship-hero .category-hero-shell {
  padding-bottom: 1.25rem;
  gap: clamp(2rem, 5vw, 3.5rem);
}

.sponsorship-hero-copy .hero-kicker {
  margin-bottom: 0.5rem;
}

.sponsorship-hero-copy h1 {
  font-size: var(--display-lg);
}

.sponsorship-proof {
  margin-top: 1.6rem;
}

.sponsorship-proof .proof-sep {
  color: oklch(100% 0 0 / 0.32);
  margin-inline: 0.15rem;
}

.sponsorship-hero .hero-actions {
  margin-top: 1.9rem;
}

.sponsorship-section {
  --section-pad: clamp(2.75rem, 5.5vw, 4.25rem);
  padding-block: var(--section-pad);
  border-bottom: 1px solid var(--line);
}

/* Sections that open with a label but end with a box get the space the label's line adds above its text */
.sponsorship-audience,
.sponsorship-getstarted {
  padding-bottom: calc(var(--section-pad) + 0.5rem);
}

.sponsorship-independence {
  padding-bottom: calc(var(--section-pad) + 0.25rem);
}

.sponsorship-section:last-of-type {
  border-bottom: 0;
}

.sponsorship-getstarted {
  background: var(--cta-bg);
  border-top: 1px solid var(--line);
}

.sponsorship-shell {
  display: grid;
  grid-template-columns: minmax(0, 16rem) minmax(0, 1fr);
  gap: clamp(1.75rem, 5vw, 4rem);
  align-items: start;
}

.sponsorship-meta {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  position: sticky;
  top: 1.5rem;
}

.sponsorship-meta .section-label {
  margin-bottom: 0;
  font-size: var(--text-lg);
}

.sponsorship-meta-note {
  color: var(--ink-muted);
  font-size: var(--text-sm);
  line-height: 1.55;
}

.sponsorship-body {
  display: flex;
  flex-direction: column;
  gap: 1.6rem;
  font-size: var(--text-lg);
  color: var(--ink-soft);
  line-height: 1.7;
}

.sponsorship-body p {
  text-wrap: pretty;
}

.sponsorship-body code {
  font-family: ui-monospace, "SFMono-Regular", "Menlo", monospace;
  font-size: 0.92em;
  padding: 0.08rem 0.4rem;
  border-radius: 0.4rem;
  background: var(--bg-paper-strong);
  color: var(--ink);
}

.sponsorship-body a:not(.hero-action):not(.tier-cta) {
  color: var(--accent-deep);
  text-decoration: underline;
  text-decoration-color: var(--accent-underline);
  text-underline-offset: 0.2em;
  transition: color 180ms ease;
}

.sponsorship-body a:not(.hero-action):not(.tier-cta):hover {
  color: var(--accent);
}

/* With the <wbr> after "@", the address breaks only there, never at the domain's hyphen */
.email-domain {
  white-space: nowrap;
}

.sponsorship-lede {
  font-size: var(--text-2xl);
  line-height: 1.45;
  color: var(--ink);
  text-wrap: pretty;
}

.sponsorship-facts {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 1.4rem;
  border-top: 1px solid var(--line);
  padding-top: 1.6rem;
}

.sponsorship-facts > div {
  display: grid;
  grid-template-columns: minmax(0, 12rem) minmax(0, 1fr);
  gap: clamp(1rem, 3vw, 2rem);
  align-items: baseline;
}

.sponsorship-facts dt {
  font-size: var(--text-sm);
  font-weight: 800;
  letter-spacing: 0.04em;
  color: var(--ink);
}

.sponsorship-facts dd {
  color: var(--ink-soft);
  font-size: var(--text-base);
  line-height: 1.65;
}

.tier-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: clamp(1.5rem, 3vw, 2.75rem);
}

.tier {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-block: 1.65rem;
  border-top: 1px solid var(--line-strong);
}

.tier-eyebrow {
  font-size: var(--text-sm);
  font-weight: 800;
  letter-spacing: 0.04em;
  color: var(--ink);
}

.tier-price {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 0.35rem 0.55rem;
  margin-bottom: 0.25rem;
}

.tier-amount {
  font-family: var(--font-display);
  font-size: clamp(3rem, 5.5vw, 4.5rem);
  font-weight: 600;
  line-height: 0.9;
  letter-spacing: -0.025em;
  font-variant-numeric: lining-nums;
  color: var(--ink);
}

.tier-cadence {
  color: var(--ink-muted);
  font-size: var(--text-base);
  font-weight: 600;
  letter-spacing: 0.01em;
}

.tier-summary {
  font-size: var(--text-lg);
  color: var(--ink);
  line-height: 1.5;
  text-wrap: pretty;
}

.tier-includes {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  border-top: 1px solid var(--line);
  padding-top: 1.1rem;
}

.tier-includes li {
  position: relative;
  padding-left: 1.4rem;
  color: var(--ink-soft);
  font-size: var(--text-base);
  line-height: 1.6;
}

.tier-includes li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.65rem;
  width: 0.55rem;
  height: 1px;
  background: var(--line-strong);
}

.tier-cta {
  align-self: start;
  margin-top: 0.75rem;
  color: var(--accent-deep);
  font-size: var(--text-sm);
  font-weight: 700;
  letter-spacing: 0.01em;
  text-decoration: underline;
  text-decoration-color: var(--accent-underline);
  text-underline-offset: 0.22em;
  transition: color 180ms ease, text-decoration-color 180ms ease;
}

.tier-cta:hover {
  color: var(--accent);
  text-decoration-color: var(--accent);
}

.past-sponsors {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.past-sponsors li {
  display: flex;
  flex-direction: column;
  align-items: start;
  gap: 0.35rem;
  padding-block: 0.4rem;
}

.past-sponsors a {
  font-family: var(--font-display);
  font-size: var(--display-sm);
  font-weight: 600;
  line-height: 1;
  letter-spacing: -0.02em;
  color: var(--ink);
  transition: color 180ms ease;
}

.past-sponsors a:hover {
  color: var(--accent-deep);
}

.past-sponsor-desc {
  color: var(--ink-soft);
  font-size: var(--text-lg);
}

.sponsorship-cta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
  margin-top: 0.5rem;
}

.sponsorship-cta-row .hero-action-primary {
  color: var(--hero-text);
  background: linear-gradient(135deg, var(--accent), var(--accent-deep));
}

.sponsorship-fineprint {
  font-size: var(--text-base);
  color: var(--ink-muted);
}

.final-cta {
  /* The extra 0.5rem matches the space above the label's first line */
  padding-block: var(--shell-pad) calc(var(--shell-pad) + 0.5rem);
  background: var(--cta-bg);
}

.final-cta > .section-shell {
  display: grid;
  gap: 1rem;
}

.final-cta .section-label {
  margin-bottom: 0;
}

.final-cta p {
  color: var(--ink-soft);
  font-size: var(--text-lg);
}

.final-cta .hero-action-primary {
  color: var(--hero-text);
  background: linear-gradient(135deg, var(--accent), var(--accent-deep));
}

.final-cta .hero-action-secondary {
  color: var(--ink);
  background: transparent;
  border-color: var(--line-strong);
}

.final-cta .hero-action-secondary:hover {
  background: var(--accent-soft);
  border-color: var(--accent);
}

.footer {
  margin-top: auto;
  background: var(--footer-bg);
  padding: 3rem var(--shell-pad);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  font-size: var(--text-sm);
  color: var(--footer-text);
}

.footer a {
  color: var(--footer-link);
}

.footer a:hover {
  color: var(--footer-link-hover);
  text-decoration: underline;
  text-decoration-color: oklch(95% 0.01 80 / 0.4);
  text-underline-offset: 0.2em;
}

.footer-left {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.footer-brand {
  font-weight: 700;
  letter-spacing: 0.03em;
  color: var(--footer-link);
}

.footer-links {
  display: block;
  text-align: right;
}

.footer-sep {
  color: var(--footer-sep);
}

.noscript-msg {
  padding: 1rem var(--shell-pad) 0;
  text-align: center;
  color: var(--ink-muted);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

@keyframes expand-in {
  from {
    opacity: 0;
    transform: translateY(-0.4rem);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 960px) {
  .hero-grid,
  .results-intro,
  .sponsor-shell,
  .sponsorship-shell {
    grid-template-columns: 1fr;
  }

  /* Stacked, the band opens with its label instead of the sponsor name */
  .sponsor-band {
    padding-bottom: var(--band-pad);
  }

  /* Stacked, the tiers open with their label instead of a tier box */
  .sponsorship-tiers {
    padding-bottom: calc(var(--section-pad) + 0.5rem);
  }

  .sponsor-meta {
    flex-direction: row;
    justify-content: space-between;
    align-items: baseline;
  }

  .sponsor-link {
    margin-block-start: 0;
  }

  .sponsorship-meta {
    position: static;
  }

  .tier-list {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .sponsorship-facts > div {
    grid-template-columns: 1fr;
    gap: 0.35rem;
  }

  .hero-category-details {
    grid-template-columns: 1fr;
    gap: 0.95rem;
  }

  .hero-category-links {
    columns: 10rem;
  }

  .results-note {
    justify-self: start;
  }

  .col-commit,
  .col-stars {
    display: none;
  }

  .expand-commit,
  .expand-stars {
    display: inline;
  }

  .tag-group {
    display: none;
  }

  .tag {
    padding: 0.38rem 0.65rem;
    font-size: var(--text-xs);
  }

  .table-wrap {
    overflow-x: clip;
  }
}

@media (max-width: 680px) {
  .proof-stat {
    display: block;
  }

  .proof-sep {
    display: none;
  }

  .hero-topbar {
    gap: 0.75rem;
  }

  .footer {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .hero-actions,
  .final-cta-actions {
    width: 100%;
  }

  .hero-topbar-actions {
    width: auto;
    flex: 0 0 auto;
  }

  .hero-topbar-link {
    width: auto;
    white-space: nowrap;
  }

  .hero-action {
    width: 100%;
  }

  .hero h1 {
    font-size: clamp(3.6rem, 18vw, 5.2rem);
  }

  .hero-category-links {
    columns: 8rem;
    column-gap: 0.75rem;
  }

  .search {
    min-height: 3.5rem;
    border-radius: 1.25rem;
  }

  .table thead th,
  .table tbody td {
    padding-inline: 0.55rem;
  }

  .table thead th:first-child,
  .table tbody td:first-child,
  .table thead th.col-name,
  .table tbody td.col-name,
  .table .desc-row td[colspan],
  .group-row th {
    padding-left: 0.8rem;
  }

  .table thead th:last-child,
  .table tbody td:last-child,
  .group-row th {
    padding-right: 0.8rem;
  }

  .col-num,
  .col-cat {
    display: none;
  }

  .expand-row td:first-child,
  .expand-row td:last-child {
    display: none;
  }

  .col-name {
    white-space: normal;
  }

  .mobile-cat {
    display: block;
    margin-top: 0.25rem;
    font-size: var(--text-xs);
    font-weight: 600;
    color: var(--ink-muted);
  }

  .expand-row td[colspan] {
    padding-left: 0.8rem;
    padding-right: 0.8rem;
  }

  /* Start the stars and commit time on their own line instead of wrapping mid-phrase after the URL */
  .expand-stars::before {
    content: "\A";
    white-space: pre;
  }

  .expand-stars > .expand-sep {
    display: none;
  }

  .col-downloads {
    width: 7.5rem;
  }

  .col-arrow {
    width: 1.8rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  html {
    scroll-behavior: auto;
  }

  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}



================================================
FILE: website/templates/_sponsor_band.html
================================================
{% if sponsors %}
<section class="sponsor-band" aria-labelledby="sponsor-heading">
  <div class="section-shell sponsor-shell">
    <header class="sponsor-meta">
      <p class="section-label" id="sponsor-heading">Sponsors</p>
      <a class="sponsor-become" href="/sponsorship/"> Become a sponsor </a>
    </header>
    <ul class="sponsor-list">
      {% for sponsor in sponsors %}
      <li class="sponsor">
        <a
          class="sponsor-link"
          href="{{ sponsor.url }}"
          target="_blank"
          rel="noopener"
        >
          <span class="sponsor-name">{{ sponsor.name }}</span>
        </a>
        <p class="sponsor-desc">{{ sponsor.description | safe }}</p>
      </li>
      {% endfor %}
    </ul>
  </div>
</section>
{% endif %}



================================================
FILE: website/templates/base.html
================================================
<!doctype html>
<html lang="en">
  <head>
    {% set default_meta_title = "Awesome Python" %}
    {% set default_meta_description = "An opinionated guide to the best Python frameworks, libraries, and tools. Explore " ~ (entries | length) ~ " curated projects across " ~ total_categories ~ " categories, from AI and agents to data science and web development." %}
    {% set default_canonical_url = "https://awesome-python.com/" %}
    {% set social_image_url = "https://awesome-python.com/static/og-image.png" %}
    {% set meta_title %}{% block title %}{{ default_meta_title }}{% endblock %}{% endset %}
    {% set meta_description %}{% block description %}{{ default_meta_description }}{% endblock %}{% endset %}
    {% set canonical_url %}{% block canonical_url %}{{ default_canonical_url }}{% endblock %}{% endset %}
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{ meta_title | trim }}</title>
    <meta name="description" content="{{ meta_description | trim }}" />
    <link rel="canonical" href="{{ canonical_url | trim }}" />
    {% block alternate_links %}
    <link rel="alternate" type="text/plain" href="/llms.txt" title="LLMs text entry point" />
    {% endblock %}
    <meta property="og:type" content="website" />
    <meta property="og:title" content="{{ meta_title | trim }}" />
    <meta property="og:description" content="{{ meta_description | trim }}" />
    <meta property="og:image" content="{{ social_image_url }}" />
    <meta property="og:url" content="{{ canonical_url | trim }}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{{ meta_title | trim }}" />
    <meta name="twitter:description" content="{{ meta_description | trim }}" />
    <meta name="twitter:image" content="{{ social_image_url }}" />
    <meta name="theme-color" content="#1c1410" />
    <link rel="icon" href="/static/favicon.svg" type="image/svg+xml" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Manrope:wght@400;600;700;800&display=swap"
      rel="stylesheet"
      media="print"
      onload="this.media = 'all'"
    />
    <noscript
      ><link
        href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Manrope:wght@400;600;700;800&display=swap"
        rel="stylesheet"
    /></noscript>
    <link rel="stylesheet" href="/static/style.css" />
    <script
      async
      src="https://www.googletagmanager.com/gtag/js?id=G-0LMLYE0HER"
    ></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag() {
        dataLayer.push(arguments);
      }
      gtag("js", new Date());
      gtag("config", "G-0LMLYE0HER");
    </script>
    {% block extra_head %}{% endblock %}
  </head>
  <body>
    <a href="#content" class="skip-link">Skip to content</a>

    {% block header %}{% endblock %}
    <main id="content">
      <noscript
        ><p class="noscript-msg">
          Search, sorting, and row details need JavaScript. The full list is also on
          <a href="https://github.com/vinta/awesome-python">GitHub</a>.
        </p></noscript
      >
      {% block content %}{% endblock %}
    </main>

    <footer class="footer">
      <div class="footer-left">
        <a href="/" class="footer-brand">Awesome Python</a>
        <span class="footer-sep">/</span>
        <a href="/sponsorship/">Sponsorship</a>
      </div>
      <div class="footer-links">
        <span
          >Made by
          <a href="https://vinta.ws/" target="_blank" rel="noopener"
            >Vinta</a
          ></span
        >
        <span class="footer-sep">/</span>
        <a href="https://github.com/vinta" target="_blank" rel="noopener"
          >GitHub</a
        >
        <span class="footer-sep">/</span>
        <a href="https://x.com/vinta" target="_blank" rel="noopener"
          >X (Twitter)</a
        >
      </div>
    </footer>

    <script src="/static/main.js"></script>
  </body>
</html>



================================================
FILE: website/templates/category.html
================================================
{% extends "base.html" %}
{% block title %}{{ category_title }}{% endblock %}
{% block description %}{{ category_description }}{% endblock %}
{% block canonical_url %}{{ category_url }}{% endblock %}
{% block alternate_links %}{% endblock %}
{% block extra_head %}
<script type="application/ld+json">{{ category_json_ld | safe }}</script>
{% endblock %}
{% block header %}
<header class="category-hero">
  <div class="hero-noise" aria-hidden="true"></div>

  <div class="category-hero-shell">
    <nav class="hero-topbar category-topbar" aria-label="Site">
      <a href="/" class="hero-brand-mini">Awesome Python</a>
      <div class="hero-topbar-actions">
        <a href="/#library-index" class="hero-topbar-link">All projects</a>
        <a
          href="https://github.com/vinta/awesome-python/blob/master/CONTRIBUTING.md"
          class="hero-topbar-link hero-topbar-link-strong"
          target="_blank"
          rel="noopener"
          >Submit a project</a
        >
        <a href="/sponsorship/" class="hero-topbar-link">Sponsorship</a>
      </div>
    </nav>

    <div class="category-hero-copy">
      {% if parent_category %}
      <p class="category-breadcrumb">
        <a href="/categories/{{ parent_category.slug }}/">{{ parent_category.name }}</a>
      </p>
      {% endif %}
      <h1>{{ category.name }}</h1>
      {% if category.description_html %}
      <p class="category-subtitle">{{ category.description_html | safe }}</p>
      {% endif %}
      {% if intro_html %}
      <div class="category-intro">{{ intro_html | safe }}</div>
      {% endif %}
      {% set named_groups = entry_groups | selectattr("name") | list %}
      {% if (named_groups and not group_categories) or guide_html %}
      <nav class="jump-links" aria-label="On this page">
        {% if not group_categories %}
        {% for group in named_groups %}
        <a class="jump-link" href="#{{ group.slug }}">{{ group.name }}</a>
        {% endfor %}
        {% endif %}
        {% if guide_html %}
        <a class="jump-link" href="#guide">{{ category.name }} guide</a>
        {% endif %}
      </nav>
      {% endif %}
    </div>

    {% if group_categories %}
    <nav class="hero-category-nav" aria-labelledby="hero-category-heading">
      <div class="hero-category-meta">
        <h2 id="hero-category-heading">Browse by category</h2>
      </div>
      <ul class="hero-category-links">
        {% for sub in group_categories %}
        <li>
          <a class="hero-category-link" href="{{ category_urls[sub.name] }}"
            >{{ sub.name }}</a
          >
        </li>
        {% endfor %}
      </ul>
    </nav>
    {% endif %}
  </div>
</header>
{% endblock %}
{% block content %}
{% macro entry_rows(entry, index) %}
        {# On section and subcategory pages the group heading already names the row's use case #}
        {% set grouped_page = entry_groups and not group_categories %}
        {% set section_path = "/categories/" ~ parent_category.slug ~ "/" if parent_category else current_path %}
        <tr
          class="row"
          {% if not group_categories %}id="entry-{{ entry.name | slugify }}"{% endif %}
          tabindex="0"
          aria-expanded="false"
          aria-controls="expand-{{ index }}"
        >
          <td class="col-num">{{ index }}</td>
          <td class="col-name">
            <a href="{{ entry.url }}" target="_blank" rel="noopener"
              >{{ entry.name }}</a
            >
            <span class="mobile-cat{% if grouped_page and (not entry.subcategories or category_urls[entry.subcategories[0].value.split(' > ')[0]] == section_path) %} repeats-heading{% endif %}"
              >{% if entry.subcategories %}{{ entry.subcategories[0].name }}{%
              else %}{{ category.name }}{% endif %}</span
            >
          </td>
          <td class="col-downloads">
            {% if entry.downloads is not none %}{{
            "{:,}".format(entry.downloads) }}{% elif entry.source_type ==
            'Stdlib' %}<span class="source-badge">Stdlib</span>{% elif
            entry.bundled %}<span class="source-badge">Bundled</span>{% elif
            entry.badge %}<span class="source-badge">{{ entry.badge }}</span>{%
            else %}<span class="source-badge">Not on PyPI</span>{% endif %}
          </td>
          <td class="col-stars">
            {% if entry.stars is not none %}{{ "{:,}".format(entry.stars) }}{%
            elif entry.source_type %}<span class="source-badge"
              >{{ entry.source_type }}</span
            >{% else %}&mdash;{% endif %}
          </td>
          <td
            class="col-commit"
            {%
            if
            entry.last_commit_at
            %}data-commit="{{ entry.last_commit_at }}"
            {%
            endif
            %}
          >
            {% if entry.last_commit_at %}<time
              datetime="{{ entry.last_commit_at }}"
              >{{ entry.last_commit_at[:10] }}</time
            >{% else %}&mdash;{% endif %}
          </td>
          <td class="col-cat">
            {% for subcat in entry.subcategories %}
            <a class="tag{% if subcat.url == current_path %} active{% endif %}{% if grouped_page and category_urls[subcat.value.split(' > ')[0]] == section_path %} repeats-heading{% endif %}" href="{{ category_urls[subcat.value.split(' > ')[0]] }}#{{ subcat.slug }}">
              {{ subcat.name }}
            </a>
            {% endfor %}
            {% for cat in entry.categories %}
            <a
              class="tag{% if category_urls[cat] == current_path %} active{% endif %}{% if grouped_page and category_urls[cat] == current_path %} repeats-heading{% endif %}"
              href="{{ category_urls[cat] }}"
              >{{ cat }}</a
            >
            {% endfor %}
            {% if entry.groups %}
            {% set group_url = filter_urls[entry.groups[0]] %}
            <a
              class="tag tag-group{% if group_url == current_path %} active{% endif %}"
              href="{{ group_url }}"
            >
              {{ entry.groups[0] }}
            </a>
            {% endif %}
            {% if entry.source_type == 'Stdlib' %}
            <a
              class="tag tag-source{% if '/categories/built-in/' == current_path %} active{% endif %}"
              href="/categories/built-in/"
            >
              Stdlib
            </a>
            {% endif %}
          </td>
          <td class="col-arrow"><span class="arrow">&rarr;</span></td>
        </tr>
        {% if entry.description %}
        <tr class="desc-row">
          <td class="col-num"></td>
          <td colspan="6">
            <div class="desc-text">{{ entry.description | safe }}</div>
          </td>
        </tr>
        {% endif %}
        <tr class="expand-row" id="expand-{{ index }}">
          <td></td>
          <td colspan="5">
            <div class="expand-content">
              {% if entry.also_see %}
              <div class="expand-also-see">
                Also see: {% for see in entry.also_see %}<a
                  href="{{ see.url }}"
                  target="_blank"
                  rel="noopener"
                  >{{ see.name }}</a
                >{% if not loop.last %}, {% endif %}{% endfor %}
              </div>
              {% endif %}
              <div class="expand-meta">
                {% if entry.owner %}<a
                  href="https://github.com/{{ entry.owner }}"
                  target="_blank"
                  rel="noopener"
                  >{{ entry.owner }}</a
                ><span class="expand-sep">/</span>{% endif %}<a
                  href="{{ entry.url }}"
                  target="_blank"
                  rel="noopener"
                  >{{ entry.url | replace("https://", "") }}</a
                >
                {% if entry.stars is not none %}<span
                  class="expand-stars"
                  ><span class="expand-sep">/</span>{{
                  "{:,}".format(entry.stars) }} stars</span
                >{% endif %} {% if entry.last_commit_at %}<span class="expand-commit"
                  ><span class="expand-sep">/</span
                  ><time datetime="{{ entry.last_commit_at }}"
                    >{{ entry.last_commit_at[:10] }}</time
                  ></span
                >{% endif %}
              </div>
            </div>
          </td>
          <td></td>
        </tr>
{% endmacro %}
{% include "_sponsor_band.html" %}

<section class="results-section" id="library-index">
  {% set single_entry = entries | length == 1 %}
  <div class="results-intro section-shell">
    {% if entry_groups and not single_entry %}
    {% set named_groups = entry_groups | selectattr("name") | list %}
    <p class="order-note">
      {% if group_categories %}Listed by section, in editorial order.{% elif named_groups %}Listed in editorial order, grouped by use case.{% else %}Listed in editorial order.{% endif %}
      <strong>Click a column header</strong> to re-sort the whole list.
    </p>
    {% elif not entry_groups %}
    <div>
      <h2>{{ entries | length }} {{ category.name }} project{{ "s" if not single_entry }}</h2>
    </div>
    {% endif %}
    <p class="results-note">
      {% if not single_entry %}Press <kbd>/</kbd> to search. {% endif %}Tags open their category. Click a row for
      details.
    </p>
  </div>

  <div class="controls section-shell">
    <h2 class="sr-only">Search and filter</h2>
    <div class="search-wrap">
      <svg
        class="search-icon"
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <circle cx="11" cy="11" r="8" />
        <line x1="21" y1="21" x2="16.65" y2="16.65" />
      </svg>
      <input
        type="search"
        class="search"
        placeholder="Search {{ entries | length }} project{{ "s" if not single_entry }} in {{ category.name }}…"
        data-short-placeholder="Search {{ entries | length }} project{{ "s" if not single_entry }}…"
        aria-label="Search projects"
      />
    </div>
  </div>

  <h2 class="sr-only">Results</h2>
  <div
    class="table-wrap"
    tabindex="0"
    role="region"
    aria-label="Projects table"
  >
    <table class="table"{% if entry_groups %} data-default-sort="editorial"{% endif %}>
      <thead>
        <tr>
          <th class="col-num"><span class="sr-only">Row number</span></th>
          <th class="col-name" data-sort="name">
            <button type="button" class="sort-btn">Project Name</button>
          </th>
          <th class="col-downloads" data-sort="downloads">
            <button type="button" class="sort-btn" title="PyPI downloads, last 30 days">PyPI Downloads</button>
          </th>
          <th class="col-stars" data-sort="stars">
            <button type="button" class="sort-btn">GitHub Stars</button>
          </th>
          <th class="col-commit" data-sort="commit-time">
            <button type="button" class="sort-btn">Last Commit</button>
          </th>
          <th class="col-cat">Tags</th>
          <th class="col-arrow">
            <button class="back-to-top" aria-label="Back to top">
              Top &uarr;
            </button>
          </th>
        </tr>
      </thead>
      <tbody>
        {% if entry_groups %}
        {% set row = namespace(index=0) %}
        {% for group in entry_groups %}
        {% if group.name %}
        <tr class="group-row">
          <th colspan="7" scope="rowgroup">
            <h2 id="{{ group.slug }}">
              {% if group.url %}<a href="{{ group.url }}">{{ group.name }}</a>{% else %}{{ group.name }}{% endif %}
              <span class="group-count">{{ group.entries | length }} project{{ "s" if group.entries | length != 1 }}</span>
            </h2>
            {% if group.lead %}
            <div class="group-lead">{{ group.lead | safe }}</div>
            {% endif %}
          </th>
        </tr>
        {% endif %}
        {% for entry in group.entries %}
        {% set row.index = row.index + 1 %}
        {{ entry_rows(entry, row.index) }}
        {% endfor %}
        {% endfor %}
        {% else %}
        {% for entry in entries %}
        {{ entry_rows(entry, loop.index) }}
        {% endfor %}
        {% endif %}
      </tbody>
    </table>
  </div>

  <div class="no-results" hidden>
    <p>No projects match your search.</p>
    <p class="no-results-hint">
      Try a broader term, or
      <button class="no-results-clear">browse all projects</button>.
    </p>
  </div>
</section>

{% if guide_html %}
<section class="guide-band" id="guide">
  <div class="guide-section section-shell">
    <h2>{{ category.name }} guide</h2>
    <div class="guide-body">{{ guide_html | safe }}</div>
  </div>
</section>
{% endif %}

<section class="final-cta">
  <div class="section-shell">
    <p class="section-label">Contribute</p>
    <h2>Know a project that belongs here?</h2>
    <p>Tell us what it does and why it stands out.</p>
    <div class="final-cta-actions">
      <a
        href="https://github.com/vinta/awesome-python/blob/master/CONTRIBUTING.md"
        class="hero-action hero-action-primary"
        target="_blank"
        rel="noopener"
        >Submit a project</a
      >
      <a
        href="https://github.com/vinta/awesome-python"
        class="hero-action hero-action-secondary"
        target="_blank"
        rel="noopener"
        >Star the repository</a
      >
    </div>
  </div>
</section>
{% endblock %}



================================================
FILE: website/templates/index.html
================================================
{% extends "base.html" %}
{% block extra_head %}
<script type="application/ld+json">{{ homepage_json_ld | safe }}</script>
{% endblock %}
{% block header %}
<header class="hero">
  <div class="hero-noise" aria-hidden="true"></div>

  <div class="hero-shell">
    <nav class="hero-topbar" aria-label="Site">
      <span class="hero-brand-mini">Awesome Python</span>
      <div class="hero-topbar-actions">
        <a
          href="https://github.com/vinta/awesome-python/blob/master/CONTRIBUTING.md"
          class="hero-topbar-link hero-topbar-link-strong"
          target="_blank"
          rel="noopener"
          >Submit a project</a
        >
        <a href="/sponsorship/" class="hero-topbar-link">Sponsorship</a>
      </div>
    </nav>

    <div class="hero-grid">
      <div class="hero-copy">
        <p class="hero-kicker">Answers “I want to do X in Python. Which tool should I use?”</p>
        <h1>Awesome Python</h1>
        <p class="hero-sub">{{ subtitle }}</p>
        <p class="hero-proof">
          {% if repo_stars %}<span class="proof-stat">{{ repo_stars }}+ stars on GitHub</span> <span class="proof-sep">/</span>{% endif %} <span class="proof-stat">Maintained by
          <a href="https://github.com/vinta" target="_blank" rel="noopener">@vinta</a>
          and
          <a href="https://github.com/JinyangWang27" target="_blank" rel="noopener">@JinyangWang27</a></span>
        </p>
        <div class="hero-actions">
          <a
            href="#library-index"
            class="hero-action hero-action-primary"
            data-scroll-to="library-index"
            >Browse the list</a
          >
          <a
            href="https://github.com/vinta/awesome-python"
            class="hero-action hero-action-secondary"
            target="_blank"
            rel="noopener"
            >View on GitHub</a
          >
        </div>
      </div>
    </div>

    <nav class="hero-category-nav" aria-labelledby="hero-category-heading">
      <details class="hero-category-details" open>
        <summary class="hero-category-meta">
          <h2 id="hero-category-heading">Browse by category</h2>
        </summary>
        <ul class="hero-category-links">
          {% for category in categories %}
          <li>
            <a class="hero-category-link" href="{{ category_urls[category.name] }}"
              >{{ category.name }}</a
            >
          </li>
          {% endfor %}
        </ul>
      </details>
      <script>
        // Collapse before first paint on phones, where the open list pushes the table about 1.5 screens down
        if (matchMedia("(max-width: 680px)").matches) {
          document.currentScript.previousElementSibling.open = false;
        }
      </script>
    </nav>
  </div>
</header>
{% endblock %}
{% block content %}
{% include "_sponsor_band.html" %}

<section class="results-section" id="library-index">
  <div class="results-intro section-shell">
    <div>
      <h2>Search projects in one place</h2>
    </div>
    <p class="results-note">
      Press <kbd>/</kbd> to search. Tags open their category. Click a row for
      details.
    </p>
  </div>

  <div class="controls section-shell">
    <h2 class="sr-only">Search and filter</h2>
    <div class="search-wrap">
      <svg
        class="search-icon"
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <circle cx="11" cy="11" r="8" />
        <line x1="21" y1="21" x2="16.65" y2="16.65" />
      </svg>
      <input
        type="search"
        class="search"
        placeholder="Search {{ entries | length }} projects across {{ total_categories }} categories…"
        data-short-placeholder="Search {{ entries | length }} projects…"
        aria-label="Search projects"
      />
    </div>
  </div>

  <h2 class="sr-only">Results</h2>
  <div
    class="table-wrap"
    tabindex="0"
    role="region"
    aria-label="Projects table"
  >
    <table class="table">
      <thead>
        <tr>
          <th class="col-num"><span class="sr-only">Row number</span></th>
          <th class="col-name" data-sort="name">
            <button type="button" class="sort-btn">Project Name</button>
          </th>
          <th class="col-downloads" data-sort="downloads">
            <button type="button" class="sort-btn" title="PyPI downloads, last 30 days">PyPI Downloads</button>
          </th>
          <th class="col-stars" data-sort="stars">
            <button type="button" class="sort-btn">GitHub Stars</button>
          </th>
          <th class="col-commit" data-sort="commit-time">
            <button type="button" class="sort-btn">Last Commit</button>
          </th>
          <th class="col-cat">Tags</th>
          <th class="col-arrow">
            <button class="back-to-top" aria-label="Back to top">
              Top &uarr;
            </button>
          </th>
        </tr>
      </thead>
      <tbody>
        {% for entry in entries %}
        <tr
          class="row"
          tabindex="0"
          aria-expanded="false"
          aria-controls="expand-{{ loop.index }}"
        >
          <td class="col-num">{{ loop.index }}</td>
          <td class="col-name">
            <a href="{{ entry.url }}" target="_blank" rel="noopener"
              >{{ entry.name }}</a
            >
            <span class="mobile-cat"
              >{% if entry.subcategories %}{{ entry.subcategories[0].name }}{%
              else %}{{ entry.categories[0] }}{% endif %}</span
            >
          </td>
          <td class="col-downloads">
            {% if entry.downloads is not none %}{{
            "{:,}".format(entry.downloads) }}{% elif entry.source_type ==
            'Stdlib' %}<span class="source-badge">Stdlib</span>{% elif
            entry.bundled %}<span class="source-badge">Bundled</span>{% elif
            entry.badge %}<span class="source-badge">{{ entry.badge }}</span>{%
            else %}<span class="source-badge">Not on PyPI</span>{% endif %}
          </td>
          <td class="col-stars">
            {% if entry.stars is not none %}{{ "{:,}".format(entry.stars) }}{%
            elif entry.source_type %}<span class="source-badge"
              >{{ entry.source_type }}</span
            >{% else %}&mdash;{% endif %}
          </td>
          <td
            class="col-commit"
            {%
            if
            entry.last_commit_at
            %}data-commit="{{ entry.last_commit_at }}"
            {%
            endif
            %}
          >
            {% if entry.last_commit_at %}<time
              datetime="{{ entry.last_commit_at }}"
              >{{ entry.last_commit_at[:10] }}</time
            >{% else %}&mdash;{% endif %}
          </td>
          <td class="col-cat">
            {% for subcat in entry.subcategories %}
            <a class="tag" href="{{ category_urls[subcat.value.split(' > ')[0]] }}#{{ subcat.slug }}">
              {{ subcat.name }}
            </a>
            {% endfor %} {% for cat in entry.categories %}
            <a
              class="tag"
              href="{{ category_urls[cat] }}"
              >{{ cat }}</a
            >
            {% endfor %}
            <a
              class="tag tag-group"
              href="{{ filter_urls[entry.groups[0]] }}"
            >
              {{ entry.groups[0] }}
            </a>
            {% if entry.source_type == 'Stdlib' %}
            <a
              class="tag tag-source"
              href="/categories/built-in/"
            >
              Stdlib
            </a>
            {% endif %}
          </td>
          <td class="col-arrow"><span class="arrow">&rarr;</span></td>
        </tr>
        {% if entry.description %}
        <tr class="desc-row" hidden>
          <td class="col-num"></td>
          <td colspan="6">
            <div class="desc-text">{{ entry.description | safe }}</div>
          </td>
        </tr>
        {% endif %}
        <tr class="expand-row" id="expand-{{ loop.index }}">
          <td></td>
          <td colspan="5">
            <div class="expand-content">
              {% if entry.also_see %}
              <div class="expand-also-see">
                Also see: {% for see in entry.also_see %}<a
                  href="{{ see.url }}"
                  target="_blank"
                  rel="noopener"
                  >{{ see.name }}</a
                >{% if not loop.last %}, {% endif %}{% endfor %}
              </div>
              {% endif %}
              <div class="expand-meta">
                {% if entry.owner %}<a
                  href="https://github.com/{{ entry.owner }}"
                  target="_blank"
                  rel="noopener"
                  >{{ entry.owner }}</a
                ><span class="expand-sep">/</span>{% endif %}<a
                  href="{{ entry.url }}"
                  target="_blank"
                  rel="noopener"
                  >{{ entry.url | replace("https://", "") }}</a
                >
                {% if entry.stars is not none %}<span
                  class="expand-stars"
                  ><span class="expand-sep">/</span>{{
                  "{:,}".format(entry.stars) }} stars</span
                >{% endif %} {% if entry.last_commit_at %}<span class="expand-commit"
                  ><span class="expand-sep">/</span
                  ><time datetime="{{ entry.last_commit_at }}"
                    >{{ entry.last_commit_at[:10] }}</time
                  ></span
                >{% endif %}
              </div>
            </div>
          </td>
          <td></td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  <div class="no-results" hidden>
    <p>No projects match your search.</p>
    <p class="no-results-hint">
      Try a broader term, or
      <button class="no-results-clear">browse all projects</button>.
    </p>
  </div>
</section>

<section class="final-cta">
  <div class="section-shell">
    <p class="section-label">Contribute</p>
    <h2>Know a project that belongs here?</h2>
    <p>Tell us what it does and why it stands out.</p>
    <div class="final-cta-actions">
      <a
        href="https://github.com/vinta/awesome-python/blob/master/CONTRIBUTING.md"
        class="hero-action hero-action-primary"
        target="_blank"
        rel="noopener"
        >Submit a project</a
      >
      <a
        href="https://github.com/vinta/awesome-python"
        class="hero-action hero-action-secondary"
        target="_blank"
        rel="noopener"
        >Star the repository</a
      >
    </div>
  </div>
</section>
{% endblock %}



================================================
FILE: website/templates/llms.txt
================================================
# Awesome Python

{{ subtitle }}

{{ total_entries }} projects across {{ total_categories }} {% if total_categories == 1 %}category{% else %}categories{% endif %}, updated on {{ build_date }}.

Scan the category index, then jump to the matching section for direct project links and short descriptions. Entries end with `PyPI downloads/month: N` (last 30 days, mirrors and CI included) and `GitHub stars: N` notes in parentheses where known; treat both as popularity context, not a quality guarantee. Use the homepage for project context outside the shortlist.

## Primary Links

- Homepage: {{ site_url }}
- GitHub repository: {{ github_repo_url }}
- Contributing guide: {{ contributing_url }}
- Sponsorship: {{ sponsorship_url }}
- Sitemap: {{ sitemap_url }}

## Categories

{{ categories_md }}



================================================
FILE: website/templates/redirect.html
================================================
<!DOCTYPE html>
<html lang="en">
<meta charset="utf-8">
<title>Redirecting&hellip;</title>
<link rel="canonical" href="{{ target_url }}">
<script>location="{{ target_url }}"</script>
<meta http-equiv="refresh" content="0; url={{ target_url }}">
<h1>Redirecting&hellip;</h1>
<p>Not redirected? <a href="{{ target_url }}">Go to {{ target_url }}</a>.</p>
</html>



================================================
FILE: website/templates/sponsorship.html
================================================
{% extends "base.html" %}
{% block title %}Sponsor Awesome Python{% endblock %}
{% block description %}{{ sponsorship_description }}{% endblock %}
{% block canonical_url %}https://awesome-python.com/sponsorship/{% endblock %}
{% block alternate_links %}{% endblock %}
{% block extra_head %}
<script type="application/ld+json">{{ sponsorship_json_ld | safe }}</script>
{% endblock %}
{% block header %}
<header class="category-hero sponsorship-hero">
  <div class="hero-noise" aria-hidden="true"></div>

  <div class="category-hero-shell">
    <nav class="hero-topbar category-topbar" aria-label="Site">
      <a href="/" class="hero-brand-mini">Awesome Python</a>
      <div class="hero-topbar-actions">
        <a
          href="https://github.com/vinta/awesome-python/blob/master/CONTRIBUTING.md"
          class="hero-topbar-link hero-topbar-link-strong"
          target="_blank"
          rel="noopener"
          >Submit a project</a
        >
        <a href="/sponsorship/" class="hero-topbar-link">Sponsorship</a>
      </div>
    </nav>

    <div class="category-hero-copy sponsorship-hero-copy">
      <p class="hero-kicker">Sponsorship</p>
      <h1>Sponsor Awesome Python</h1>
      <p class="category-subtitle">
        The #10 most-starred repository on GitHub, and the list Python
        developers check when choosing what to use. Your sponsorship puts your
        product in front of them at the moment of decision. From $99 a month:
        Headline $500, Featured $200, Indie Dev $99.
      </p>

      {% if hero_stats %}
      <p class="hero-proof sponsorship-proof">
        {% for stat in hero_stats %}<span class="proof-stat">{{ stat }}</span>{% if not loop.last %}
        <span class="proof-sep">/</span> {% endif %}{% endfor %}
      </p>
      {% endif %}

      <div class="hero-actions">
        <a
          href="mailto:sponsorship@awesome-python.com?subject=Awesome%20Python%20Sponsorship"
          data-tier="general"
          class="hero-action hero-action-primary"
          >Email us</a
        >
        <a
          href="https://github.com/vinta/awesome-python/blob/master/SPONSORSHIP.md"
          class="hero-action hero-action-secondary"
          target="_blank"
          rel="noopener"
          >Full terms on GitHub</a
        >
      </div>
    </div>
  </div>
</header>
{% endblock %} {% block content %}
<section class="sponsorship-section sponsorship-audience">
  <div class="section-shell sponsorship-shell">
    <header class="sponsorship-meta">
      <p class="section-label">Audience</p>
    </header>
    <div class="sponsorship-body">
      <p class="sponsorship-lede">
        Professional Python developers evaluating libraries and tools for
        production use. Not beginners browsing tutorials. People making adoption
        decisions.
      </p>
      <dl class="sponsorship-facts">
        <div>
          <dt>Who visits</dt>
          <dd>
            Mid to senior Python developers arriving with a specific question: a
            maintained ORM, a fast HTTP client, a task queue worth running in
            production.
          </dd>
        </div>
        <div>
          <dt>Where they come from</dt>
          <dd>
            Google Search, GitHub, Reddit, YouTube, ChatGPT and other LLMs,
            Hacker News.
          </dd>
        </div>
        <div>
          <dt>Why it works</dt>
          <dd>
            Ranks on the first page of Google for "best Python libraries".
            ChatGPT and other LLMs cite it when recommending Python tools.
            Developers send it to each other.
          </dd>
        </div>
      </dl>
    </div>
  </div>
</section>

<section class="sponsorship-section sponsorship-tiers">
  <div class="section-shell sponsorship-shell">
    <header class="sponsorship-meta">
      <p class="section-label">Tiers</p>
      <p class="sponsorship-meta-note">
        One upfront payment per term. Setup takes less than 24 hours.
      </p>
    </header>
    <div class="sponsorship-body">
      <ol class="tier-list">
        <li class="tier">
          <p class="tier-eyebrow">Headline Sponsor</p>
          <p class="tier-price">
            <span class="tier-amount">$500</span>
            <span class="tier-cadence">/&nbsp;month or $4,500&nbsp;/&nbsp;year</span>
          </p>
          <p class="tier-summary">
            Logo pinned at the top of the README. Logo on the website.
          </p>
          <ul class="tier-includes">
            <li>
              Large logo and one-line description (max 120 characters) pinned at
              the very top of the README, above all project entries.
            </li>
            <li>Logo link in the sponsor section of awesome-python.com.</li>
          </ul>
          <a
            href="mailto:sponsorship@awesome-python.com?subject=Awesome%20Python%20Sponsorship%20-%20Headline%20Tier"
            data-tier="headline"
            class="tier-cta"
            >Email about Headline tier</a
          >
        </li>
        <li class="tier">
          <p class="tier-eyebrow">Featured Sponsor</p>
          <p class="tier-price">
            <span class="tier-amount">$200</span>
            <span class="tier-cadence">/&nbsp;month or $1,800&nbsp;/&nbsp;year</span>
          </p>
          <p class="tier-summary">
            Small logo and text link pinned at the top of the README. Logo and
            text link on the website.
          </p>
          <ul class="tier-includes">
            <li>
              Small logo and text entry
              (<code>[Name](URL) - Description.</code>, max 120 characters)
              pinned at the top of the README, directly below Headline sponsors.
            </li>
            <li>
              Logo and text link in the sponsor section of awesome-python.com.
            </li>
          </ul>
          <a
            href="mailto:sponsorship@awesome-python.com?subject=Awesome%20Python%20Sponsorship%20-%20Featured%20Tier"
            data-tier="featured"
            class="tier-cta"
            >Email about Featured tier</a
          >
        </li>
        <li class="tier">
          <p class="tier-eyebrow">Indie Dev Sponsor</p>
          <p class="tier-price">
            <span class="tier-amount">$99</span>
            <span class="tier-cadence">/&nbsp;month, $249&nbsp;/&nbsp;quarter, or $891&nbsp;/&nbsp;year</span>
          </p>
          <p class="tier-summary">
            Lower-cost text link for eligible indie developers and solo
            founders.
          </p>
          <ul class="tier-includes">
            <li>
              Text entry (<code>[Name](URL) - Description.</code>, max 120
              characters) in the README sponsor section, directly below Featured
              sponsors.
            </li>
            <li>Text link in the sponsor section of awesome-python.com.</li>
            <li>
              Available only to founder-led, one-person-company products. Funded
              startups, agencies, recruiters, larger companies, and products
              with enterprise sales teams should use Featured or Headline.
            </li>
          </ul>
          <a
            href="mailto:sponsorship@awesome-python.com?subject=Awesome%20Python%20Sponsorship%20-%20Indie%20Dev%20Tier"
            data-tier="indie"
            class="tier-cta"
            >Email about Indie Dev tier</a
          >
        </li>
      </ol>
    </div>
  </div>
</section>

<section class="sponsorship-section sponsorship-past">
  <div class="section-shell sponsorship-shell">
    <header class="sponsorship-meta">
      <p class="section-label">Previously sponsored by</p>
    </header>
    <div class="sponsorship-body">
      <ul class="past-sponsors">
        <li>
          <a href="https://www.warp.dev/" target="_blank" rel="noopener"
            >Warp</a
          >
          <span class="past-sponsor-desc"
            >The terminal for modern developers.</span
          >
        </li>
        <li>
          <a href="https://pyrun.dev" target="_blank" rel="noopener">pyr</a>
          <span class="past-sponsor-desc"
            >Zero-config Python project manager.</span
          >
        </li>
      </ul>
    </div>
  </div>
</section>

<section class="sponsorship-section sponsorship-getstarted">
  <div class="section-shell sponsorship-shell">
    <header class="sponsorship-meta">
      <p class="section-label">Get started</p>
    </header>
    <div class="sponsorship-body">
      <p class="sponsorship-lede">
        Email
        <a
          href="mailto:sponsorship@awesome-python.com?subject=Awesome%20Python%20Sponsorship"
          data-tier="general"
          >sponsorship@<wbr /><span class="email-domain">awesome-python.com</span></a
        >
        with the four items below.
      </p>
      <dl class="sponsorship-facts">
        <div>
          <dt>Tier</dt>
          <dd>
            Headline, Featured, or Indie Dev Sponsor.
          </dd>
        </div>
        <div>
          <dt>Content</dt>
          <dd>
            A <code>[Name](URL) - Description.</code> entry, plus a logo for
            Headline and Featured.
          </dd>
        </div>
        <div>
          <dt>Duration</dt>
          <dd>
            1, 3, 6, or 12 months. A year gets 3 months free; Indie Dev also has
            a quarterly rate.
          </dd>
        </div>
        <div>
          <dt>Payment method</dt>
          <dd>
            Card via
            <a href="https://opencollective.com/awesome-python">Open Collective</a>,
            US bank transfer (ACH/wire), or PayPal.
          </dd>
        </div>
      </dl>
      <p>
        Sponsor links carry UTM tags, so clicks show up in your own analytics as
        <code>awesome-python&nbsp;/&nbsp;sponsorship</code>.
      </p>
      <div class="sponsorship-cta-row">
        <a
          href="mailto:sponsorship@awesome-python.com?subject=Awesome%20Python%20Sponsorship"
          data-tier="general"
          class="hero-action hero-action-primary"
          >Email us</a
        >
      </div>
    </div>
  </div>
</section>

<section class="sponsorship-section sponsorship-independence">
  <div class="section-shell sponsorship-shell">
    <header class="sponsorship-meta">
      <p class="section-label">Editorial independence</p>
    </header>
    <div class="sponsorship-body">
      <p>
        Sponsorship is logo and link placement in the README header and on this
        site. It does not influence which projects are listed. We curate listings on merit through
        the normal
        <a
          href="https://github.com/vinta/awesome-python/blob/master/CONTRIBUTING.md"
          target="_blank"
          rel="noopener"
          >contribution process</a
        >.
      </p>
      <p class="sponsorship-fineprint">
        We reserve the right to request changes to sponsor text, logos, or links
        that are misleading, off-topic, or incompatible with the README
        formatting.
      </p>
    </div>
  </div>
</section>
{% endblock %}



================================================
FILE: website/tests/test_build.py
================================================
"""Tests for the build module."""

import json
import os
import re
import shutil
import subprocess
import textwrap
import xml.etree.ElementTree as ET
from datetime import UTC, date, datetime
from html.parser import HTMLParser
from pathlib import Path

import pytest

from build import (
    TemplateEntry,
    annotate_entries_with_stats,
    build,
    category_meta_title,
    detect_source_type,
    extract_entries,
    extract_github_repo,
    load_category_intro,
    load_downloads,
    load_pypi_badges,
    load_stars,
    sort_entries,
    sponsor_website_url,
    subcategory_path,
)
from readme_parser import parse_readme, slugify


class HeadMetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title_count = 0
        self.title = ""
        self.meta_by_name = {}
        self.meta_by_property = {}
        self.links_by_rel = {}
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.title_count += 1
            self._in_title = True
        elif tag == "meta":
            if "name" in attrs:
                self.meta_by_name[attrs["name"]] = attrs.get("content", "")
            if "property" in attrs:
                self.meta_by_property[attrs["property"]] = attrs.get("content", "")
        elif tag == "link" and attrs.get("rel"):
            for rel in attrs["rel"].split():
                self.links_by_rel[rel] = attrs.get("href", "")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


# ---------------------------------------------------------------------------
# slugify
# ---------------------------------------------------------------------------


class TestSlugify:
    def test_simple(self):
        assert slugify("Admin Panels") == "admin-panels"

    def test_uppercase_acronym(self):
        assert slugify("RESTful API") == "restful-api"

    def test_hyphenated_input(self):
        assert slugify("Command-line Tools") == "command-line-tools"

    def test_extra_spaces(self):
        assert slugify("  Date  and  Time  ") == "date-and-time"


class TestSubcategoryPath:
    def test_builds_path(self):
        assert subcategory_path("web-frameworks", "synchronous") == "/categories/web-frameworks/synchronous/"


# ---------------------------------------------------------------------------
# build (integration)
# ---------------------------------------------------------------------------


class TestBuild:
    @pytest.fixture(autouse=True)
    def _make_sponsorship_md(self, tmp_path):
        (tmp_path / "SPONSORSHIP.md").write_text("# Sponsorship\n", encoding="utf-8")

    def _make_repo(self, tmp_path, readme):
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        tpl_dir = tmp_path / "website" / "templates"
        tpl_dir.mkdir(parents=True)
        (tpl_dir / "base.html").write_text(
            "<!DOCTYPE html><html lang='en'><head><title>{% block title %}{% endblock %}</title>"
            "<meta name='description' content='{% block description %}{% endblock %}'>"
            "</head><body>{% block content %}{% endblock %}</body></html>",
            encoding="utf-8",
        )
        (tpl_dir / "index.html").write_text(
            '{% extends "base.html" %}{% block content %}'
            "{% for entry in entries %}"
            '<div class="row">'
            "<span>{{ entry.name }}</span>"
            "<span>{{ entry.categories | join(', ') }}</span>"
            "<span>{{ entry.groups | join(', ') }}</span>"
            "</div>"
            "{% endfor %}"
            "{% endblock %}",
            encoding="utf-8",
        )
        (tpl_dir / "category.html").write_text(
            '{% extends "base.html" %}{% block content %}<h1>{{ category.name }}</h1>{% for entry in entries %}<a href="{{ entry.url }}">{{ entry.name }}</a>{% endfor %}{% endblock %}',
            encoding="utf-8",
        )
        (tpl_dir / "sponsorship.html").write_text(
            '{% extends "base.html" %}{% block content %}<h1>Sponsor</h1>{% endblock %}',
            encoding="utf-8",
        )
        (tpl_dir / "llms.txt").write_text(
            "# Awesome Python\n\nHomepage: {{ site_url }}\n\n## Categories\n\n{{ categories_md }}\n",
            encoding="utf-8",
        )

    def _copy_real_templates(self, tmp_path):
        real_tpl = Path(__file__).parent / ".." / "templates"
        tpl_dir = tmp_path / "website" / "templates"
        shutil.copytree(real_tpl, tpl_dir)

    def test_build_creates_homepage_and_category_pages(self, tmp_path):
        readme = textwrap.dedent("""\
            # Awesome Python

            Intro.

            ## Projects

            **Tools**

            ### Widgets

            _Widget libraries. Also see [awesome-widgets](https://example.com/widgets)._

            - [w1](https://example.com) - A widget.

            ### Gadgets

            _Gadget tools._

            - [g1](https://example.com) - A gadget.

            ## Resources

            Info.

            ### Newsletters

            - [NL](https://example.com)

            ## Contributing

            Help!
        """)
        self._make_repo(tmp_path, readme)
        build(tmp_path)

        site = tmp_path / "website" / "output"
        assert (site / "index.html").exists()
        assert (site / "categories" / "widgets" / "index.html").exists()
        assert (site / "categories" / "gadgets" / "index.html").exists()

    def test_build_creates_root_discovery_files(self, tmp_path):
        readme = textwrap.dedent("""\
            # Awesome Python

            Intro.

            ## Projects

            **Tools**

            ### Widgets

            - Sync

                - [w1](https://example.com) - A widget.

            ## Contributing

            Help!
        """)
        self._make_repo(tmp_path, readme)
        start_date = datetime.now(UTC).date()
        build(tmp_path)
        end_date = datetime.now(UTC).date()

        site = tmp_path / "website" / "output"
        robots = (site / "robots.txt").read_text(encoding="utf-8")
        assert robots == ("User-agent: *\nContent-Signal: search=yes, ai-input=yes, ai-train=yes\nAllow: /\n\nSitemap: https://awesome-python.com/sitemap.xml\n")

        sitemap = ET.parse(site / "sitemap.xml")
        root = sitemap.getroot()
        ns = {"sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [loc.text or "" for loc in root.findall("sitemap:url/sitemap:loc", ns)]
        lastmods = [lastmod.text or "" for lastmod in root.findall("sitemap:url/sitemap:lastmod", ns)]

        assert root.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}urlset"
        assert locs == [
            "https://awesome-python.com/",
            "https://awesome-python.com/categories/widgets/",
            "https://awesome-python.com/categories/tools/",
            "https://awesome-python.com/categories/widgets/sync/",
            "https://awesome-python.com/sponsorship/",
        ]
        assert len(lastmods) == len(locs)
        # Outside a git repository every page falls back to the build date
        assert all(start_date <= date.fromisoformat(lastmod) <= end_date for lastmod in lastmods)
        assert all(loc.startswith("https://awesome-python.com/") for loc in locs)
        assert all("?" not in loc for loc in locs)

    def test_sitemap_lastmod_follows_git_history_of_each_page(self, tmp_path, monkeypatch):
        # Inside a git hook or `git rebase --exec`, inherited GIT_DIR points every git call below at the real repo
        for key in [k for k in os.environ if k.startswith("GIT_")]:
            monkeypatch.delenv(key)
        readme = textwrap.dedent("""\
            # Awesome Python

            Intro.

            ## Projects

            **Tools**

            ### Widgets

            - Sync

                - [w1](https://example.com/w1) - A widget.

            ### Gadgets

            - [g1](https://example.com/g1) - A gadget.

            ## Contributing

            Help!
        """)
        self._make_repo(tmp_path, readme)

        def commit(day, message):
            env = {**os.environ, "GIT_AUTHOR_DATE": f"{day}T12:00:00Z", "GIT_COMMITTER_DATE": f"{day}T12:00:00Z"}
            subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
            subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", message], cwd=tmp_path, env=env, check=True)

        subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
        commit("2024-01-01", "initial")
        (tmp_path / "README.md").write_text(readme.replace("A gadget.", "A better gadget."), encoding="utf-8")
        commit("2024-02-01", "edit gadgets")
        intros_dir = tmp_path / "website" / "data" / "category_intros"
        intros_dir.mkdir(parents=True)
        (intros_dir / "widgets.md").write_text("Use w1.\n", encoding="utf-8")
        commit("2024-03-01", "add widgets intro")
        build(tmp_path)

        sitemap = (tmp_path / "website" / "output" / "sitemap.xml").read_text(encoding="utf-8")
        lastmod_by_loc = dict(re.findall(r"<loc>https://awesome-python\.com(\S*?)</loc>\s*<lastmod>(\S+)</lastmod>", sitemap))
        assert lastmod_by_loc == {
            "/": "2024-02-01",
            "/categories/widgets/": "2024-03-01",
            "/categories/gadgets/": "2024-02-01",
            "/categories/tools/": "2024-03-01",
            "/categories/widgets/sync/": "2024-03-01",
            "/sponsorship/": "2024-01-01",
        }

    def test_build_creates_category_pages_with_metadata_and_links(self, tmp_path):
        readme = textwrap.dedent("""\
            # Awesome Python

            Intro.

            ## Projects

            **Tools**

            ## Widgets

            _Widget libraries. Also see [awesome-widgets](https://example.com/widgets)._

            - [w1](https://example.com/w1) - A widget.
            - [w2](https://github.com/owner/w2) - A starred widget.

            ## Gadgets

            _Gadget tools._

            - [g1](https://example.com/g1) - A gadget.

            # Contributing

            Help!
        """)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        self._copy_real_templates(tmp_path)

        data_dir = tmp_path / "website" / "data"
        data_dir.mkdir(parents=True)
        stars = {
            "owner/w2": {
                "stars": 42,
                "owner": "owner",
                "last_commit_at": "2026-01-01T00:00:00+00:00",
                "fetched_at": "2026-01-01T00:00:00+00:00",
            },
        }
        (data_dir / "github_stars.json").write_text(json.dumps(stars), encoding="utf-8")

        build(tmp_path)

        site = tmp_path / "website" / "output"
        index_html = (site / "index.html").read_text(encoding="utf-8")
        category_html = (site / "categories" / "widgets" / "index.html").read_text(encoding="utf-8")
        parser = HeadMetadataParser()
        parser.feed(category_html)

        assert 'href="/categories/widgets/"' in index_html
        assert parser.title.strip() == "Python Widgets Libraries - Awesome Python"
        assert parser.meta_by_name["description"] == "Widget libraries. Also see awesome-widgets. Explore 2 curated Python projects in Widgets."
        assert parser.links_by_rel["canonical"] == "https://awesome-python.com/categories/widgets/"
        assert parser.meta_by_property["og:url"] == "https://awesome-python.com/categories/widgets/"
        assert '<link rel="alternate" type="text/plain" href="/llms.txt" title="LLMs text entry point" />' not in category_html
        assert '<a href="/sponsorship/" class="hero-topbar-link">Sponsorship</a>' in category_html
        assert "<h1>Widgets</h1>" in category_html
        assert 'Widget libraries. Also see <a href="https://example.com/widgets" target="_blank" rel="noopener">awesome-widgets</a>.' in category_html
        assert 'href="https://example.com/w1"' in category_html
        assert "A widget." in category_html
        assert 'href="https://github.com/owner/w2"' in category_html
        assert '<table class="table" data-default-sort="editorial">' in category_html
        assert "42" in category_html
        assert "2026-01-01T00:00:00+00:00" in category_html

    def test_build_links_description_anchors_to_category_pages(self, tmp_path):
        readme = textwrap.dedent("""\
            # Awesome Python

            Intro.

            ## Projects

            **Tools**

            ## Audio & Video

            _Media tools._

            - [a1](https://example.com/a1) - A media tool.

            ## Widgets

            _Widget libraries. Also see [Audio & Video](#audio--video) and [Gadgets](#gadgets)._

            - [w1](https://example.com/w1) - A widget.

            # Contributing

            Help!
        """)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        self._copy_real_templates(tmp_path)

        build(tmp_path)

        category_html = (tmp_path / "website" / "output" / "categories" / "widgets" / "index.html").read_text(encoding="utf-8")
        assert 'Also see <a href="/categories/audio-video/">Audio &amp; Video</a>' in category_html
        assert '<a href="#gadgets" target="_blank" rel="noopener">Gadgets</a>' in category_html

    def test_build_creates_llms_text_alternate_without_sponsors(self, tmp_path):
        readme = textwrap.dedent("""\
            # Awesome Python

            Intro.

            ## **Sponsors**

            - **[Sponsor](https://sponsor.example.com)**: Sponsored tool.

            > Become a sponsor: [Sponsor us](SPONSORSHIP.md).

            ## Categories

            **Tools**

            - [Widgets](#widgets)

            ## Projects

            **Tools**

            ### Widgets

            - [w1](https://example.com) - A widget.
            - [w2](https://github.com/owner/w2) - A starred widget.

            ## Contributing

            Help!
        """)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        self._copy_real_templates(tmp_path)

        data_dir = tmp_path / "website" / "data"
        data_dir.mkdir(parents=True)
        stars = {
            "owner/w2": {"stars": 42, "owner": "owner", "fetched_at": "2026-01-01T00:00:00+00:00"},
        }
        (data_dir / "github_stars.json").write_text(json.dumps(stars), encoding="utf-8")
        (data_dir / "pypi_downloads.tsv").write_text(
            "name\tpackage\tdownloads\tfetched_at\nw1\tw1\t777\t2026-08-16\n",
            encoding="utf-8",
        )

        build(tmp_path)

        site = tmp_path / "website" / "output"
        index_html = (site / "index.html").read_text(encoding="utf-8")
        llms_txt = (site / "llms.txt").read_text(encoding="utf-8")

        assert '<link rel="alternate" type="text/plain" href="/llms.txt" title="LLMs text entry point" />' in index_html

        assert llms_txt.startswith("# Awesome Python\n\nIntro.\n")
        assert "2 projects across 1 category, updated on " in llms_txt
        assert "Scan the category index" in llms_txt
        assert "Homepage: https://awesome-python.com/" in llms_txt
        assert "Markdown homepage" not in llms_txt
        assert "https://awesome-python.com/index.md" not in llms_txt
        assert "GitHub repository: https://github.com/vinta/awesome-python" in llms_txt
        assert "Contributing guide: https://github.com/vinta/awesome-python/blob/master/CONTRIBUTING.md" in llms_txt
        assert "Sponsorship: https://awesome-python.com/sponsorship/" in llms_txt
        assert "Sitemap: https://awesome-python.com/sitemap.xml" in llms_txt
        assert "## Categories" in llms_txt
        assert "**Tools**" in llms_txt
        assert "- [Widgets](https://awesome-python.com/categories/widgets/)" in llms_txt
        assert "- [Widgets](#widgets)" not in llms_txt
        assert "### Widgets" in llms_txt
        assert "- [w1](https://example.com) - A widget. (PyPI downloads/month: 777)" in llms_txt
        assert "- [w2](https://github.com/owner/w2) - A starred widget. (GitHub stars: 42)" in llms_txt
        assert llms_txt != readme
        assert "# Contributing" not in llms_txt

    def test_homepage_sponsor_link_tags_website_clicks(self, tmp_path):
        readme = textwrap.dedent("""\
            # Awesome Python

            Intro.

            ## **Sponsors**

            - [Sponsor](https://sponsor.example.com/?ref=x&utm_source=awesome-python&utm_content=readme) - Sponsored tool.

            ## Projects

            **Tools**

            ## Widgets

            - [w1](https://example.com) - A widget.

            # Contributing

            Help!
        """)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        self._copy_real_templates(tmp_path)

        build(tmp_path)

        index_html = (tmp_path / "website" / "output" / "index.html").read_text(encoding="utf-8")
        assert 'href="https://sponsor.example.com/?ref=x&amp;utm_source=awesome-python&amp;utm_content=website"' in index_html
        assert "utm_content=readme" not in index_html

    def test_category_page_shows_sponsor_band(self, tmp_path):
        readme = textwrap.dedent("""\
            # Awesome Python

            Intro.

            ## **Sponsors**

            - [Sponsor](https://sponsor.example.com) - Sponsored tool.

            ## Projects

            **Tools**

            ## Widgets

            - [w1](https://example.com) - A widget.

            # Contributing

            Help!
        """)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        self._copy_real_templates(tmp_path)

        build(tmp_path)

        category_html = (tmp_path / "website" / "output" / "categories" / "widgets" / "index.html").read_text(encoding="utf-8")
        assert 'href="https://sponsor.example.com"' in category_html
        assert '<span class="sponsor-name">Sponsor</span>' in category_html

    def test_build_cleans_stale_output(self, tmp_path):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            ## Only

            - [x](https://x.com) - X.

            # Contributing

            Done.
        """)
        self._make_repo(tmp_path, readme)

        stale = tmp_path / "website" / "output" / "categories" / "stale"
        stale.mkdir(parents=True)
        (stale / "index.html").write_text("old", encoding="utf-8")

        build(tmp_path)

        assert not (tmp_path / "website" / "output" / "categories" / "stale").exists()

    def test_build_with_stars_sorts_by_stars(self, tmp_path):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            ## Stuff

            - [low-stars](https://github.com/org/low) - Low.
            - [high-stars](https://github.com/org/high) - High.
            - [no-stars](https://example.com/none) - None.

            # Contributing

            Done.
        """)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")

        # Copy real templates
        real_tpl = Path(__file__).parent / ".." / "templates"
        tpl_dir = tmp_path / "website" / "templates"
        shutil.copytree(real_tpl, tpl_dir)

        # Create mock star data
        data_dir = tmp_path / "website" / "data"
        data_dir.mkdir(parents=True)
        stars = {
            "org/high": {"stars": 5000, "owner": "org", "fetched_at": "2026-01-01T00:00:00+00:00"},
            "org/low": {"stars": 100, "owner": "org", "fetched_at": "2026-01-01T00:00:00+00:00"},
        }
        (data_dir / "github_stars.json").write_text(json.dumps(stars), encoding="utf-8")

        build(tmp_path)

        html = (tmp_path / "website" / "output" / "index.html").read_text(encoding="utf-8")
        # Star-sorted: high-stars (5000) before low-stars (100) before no-stars (None)
        assert html.index("high-stars") < html.index("low-stars")
        assert html.index("low-stars") < html.index("no-stars")
        # Formatted star counts
        assert "5,000" in html
        assert "100" in html
        # Expand content present
        assert "expand-content" in html

    def test_build_with_downloads_renders_column(self, tmp_path):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            ## Stuff

            - [My-Lib](https://github.com/org/mylib) - On PyPI.
            - [no-pypi](https://example.com/none) - Not on PyPI.
            - [asyncio](https://docs.python.org/3/library/asyncio.html) - Stdlib.
            - [my-lib.thing](https://github.com/org/mylib) - (part of My-Lib) A bundled feature.

            # Contributing

            Done.
        """)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        self._copy_real_templates(tmp_path)

        data_dir = tmp_path / "website" / "data"
        data_dir.mkdir(parents=True)
        # Keyed by normalized README display name, like fetch_pypi_downloads_via_clickpy.py writes it
        (data_dir / "pypi_downloads.tsv").write_text(
            "name\tpackage\tdownloads\tfetched_at\nasyncio\tasyncio\t26305454\t2026-08-16\nmy-lib\tmy-lib\t1234567\t2026-08-16\n",
            encoding="utf-8",
        )

        build(tmp_path)

        html = (tmp_path / "website" / "output" / "index.html").read_text(encoding="utf-8")
        assert "1,234,567" in html
        # Stdlib entries never show PyPI counts: the asyncio row is the backport package
        assert "26,305,454" not in html
        # Default sort: entries with download counts come first
        assert html.index("My-Lib") < html.index("no-pypi")
        # Each no-download entry gets the badge matching why it has no count
        assert html.count('<span class="source-badge">Stdlib</span>') == 1
        assert html.count('<span class="source-badge">Bundled</span>') == 1
        assert html.count('<span class="source-badge">Not on PyPI</span>') == 1

    def test_build_fails_when_group_and_category_slug_collide(self, tmp_path):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            **Widgets**

            ## Widgets

            - [w1](https://example.com) - W.

            # Contributing

            Done.
        """)
        self._make_repo(tmp_path, readme)
        with pytest.raises(ValueError, match="slug collision"):
            build(tmp_path)

    def test_index_contains_aligned_homepage_metadata(self, tmp_path):
        readme = (Path(__file__).parents[2] / "README.md").read_text(encoding="utf-8")
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        self._copy_real_templates(tmp_path)

        build(tmp_path)

        parsed_groups = parse_readme(readme)
        categories = [cat for group in parsed_groups for cat in group["categories"]]
        entries = extract_entries(categories, parsed_groups)
        html = (tmp_path / "website" / "output" / "index.html").read_text(encoding="utf-8")
        parser = HeadMetadataParser()
        parser.feed(html)

        expected_title = "Awesome Python"
        expected_description = f"An opinionated guide to the best Python frameworks, libraries, and tools. Explore {len(entries)} curated projects across {len(categories)} categories, from AI and agents to data science and web development."
        expected_url = "https://awesome-python.com/"
        expected_image = "https://awesome-python.com/static/og-image.png"

        assert parser.title_count == 1
        assert parser.title.strip() == expected_title
        assert parser.meta_by_name["description"] == expected_description
        assert parser.links_by_rel["canonical"] == expected_url
        assert parser.meta_by_property["og:type"] == "website"
        assert parser.meta_by_property["og:title"] == expected_title
        assert parser.meta_by_property["og:description"] == expected_description
        assert parser.meta_by_property["og:image"] == expected_image
        assert parser.meta_by_property["og:url"] == expected_url
        assert parser.meta_by_name["twitter:card"] == "summary_large_image"
        assert parser.meta_by_name["twitter:title"] == expected_title
        assert parser.meta_by_name["twitter:description"] == expected_description
        assert parser.meta_by_name["twitter:image"] == expected_image
        assert "<head>\n    <meta charset" in html
        assert '<a href="/sponsorship/" class="hero-topbar-link">Sponsorship</a>' in html
        assert 'id="hero-category-heading">Browse by category</h2>' in html
        assert 'class="hero-category-link" href="/categories/ai-and-agents/"' in html

    def test_index_contains_homepage_json_ld(self, tmp_path):
        readme = (Path(__file__).parents[2] / "README.md").read_text(encoding="utf-8")
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        self._copy_real_templates(tmp_path)

        build(tmp_path)

        parsed_groups = parse_readme(readme)
        categories = [cat for group in parsed_groups for cat in group["categories"]]
        entries = extract_entries(categories, parsed_groups)
        html = (tmp_path / "website" / "output" / "index.html").read_text(encoding="utf-8")

        marker = '<script type="application/ld+json">'
        assert marker in html
        start = html.index(marker) + len(marker)
        end = html.index("</script>", start)
        block = html[start:end]
        assert "</script>" not in block
        data = json.loads(block)

        assert data["@context"] == "https://schema.org"
        graph = {node["@type"]: node for node in data["@graph"]}
        assert set(graph) == {"WebSite", "CollectionPage"}
        assert graph["WebSite"]["url"] == "https://awesome-python.com/"
        assert graph["WebSite"]["name"] == "Awesome Python"
        assert graph["WebSite"]["@id"] == "https://awesome-python.com/#website"

        collection = graph["CollectionPage"]
        assert collection["@id"] == "https://awesome-python.com/"
        assert collection["url"] == "https://awesome-python.com/"
        assert collection["isPartOf"] == {"@type": "WebSite", "@id": graph["WebSite"]["@id"]}
        expected_description = f"An opinionated guide to the best Python frameworks, libraries, and tools. Explore {len(entries)} curated projects across {len(categories)} categories, from AI and agents to data science and web development."
        assert collection["description"] == expected_description

        item_list = collection["mainEntity"]
        assert item_list["@type"] == "ItemList"
        assert item_list["numberOfItems"] == len(entries)
        assert len(item_list["itemListElement"]) == len(entries)

        positions = [item["position"] for item in item_list["itemListElement"]]
        assert positions == list(range(1, len(entries) + 1))
        assert all(item["@type"] == "ListItem" for item in item_list["itemListElement"])
        assert all(item["url"].startswith(("http://", "https://")) for item in item_list["itemListElement"])

        rendered_names = {item["name"] for item in item_list["itemListElement"]}
        rendered_urls = {item["url"] for item in item_list["itemListElement"]}
        assert rendered_names == {e["name"] for e in entries}
        assert rendered_urls == {e["url"] for e in entries}

    def test_category_page_contains_json_ld(self, tmp_path):
        readme = textwrap.dedent("""\
            # Awesome Python

            Intro.

            ## Projects

            **Tools**

            ## Widgets

            _Widget libraries._

            - [w1](https://example.com/w1) - A widget.
            - [w2](https://github.com/owner/w2) - A starred widget.

            # Contributing

            Help!
        """)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        self._copy_real_templates(tmp_path)
        build(tmp_path)

        category_html = (tmp_path / "website" / "output" / "categories" / "widgets" / "index.html").read_text(encoding="utf-8")
        marker = '<script type="application/ld+json">'
        assert marker in category_html
        start = category_html.index(marker) + len(marker)
        end = category_html.index("</script>", start)
        block = category_html[start:end]
        assert "</script>" not in block
        data = json.loads(block)

        assert data["@context"] == "https://schema.org"
        graph = {node["@type"]: node for node in data["@graph"]}
        assert set(graph) == {"WebSite", "CollectionPage", "BreadcrumbList"}
        assert graph["WebSite"]["@id"] == "https://awesome-python.com/#website"
        collection = graph["CollectionPage"]
        assert collection["name"] == "Python Widgets Libraries"
        assert collection["@id"] == "https://awesome-python.com/categories/widgets/"
        assert collection["url"] == "https://awesome-python.com/categories/widgets/"
        assert collection["description"] == "Widget libraries. Explore 2 curated Python projects in Widgets."
        assert collection["isPartOf"] == {"@type": "WebSite", "@id": "https://awesome-python.com/#website"}

        item_list = collection["mainEntity"]
        assert item_list["@type"] == "ItemList"
        assert item_list["numberOfItems"] == 2
        names = {item["name"] for item in item_list["itemListElement"]}
        urls = {item["url"] for item in item_list["itemListElement"]}
        assert names == {"w1", "w2"}
        assert urls == {"https://example.com/w1", "https://github.com/owner/w2"}
        positions = sorted(item["position"] for item in item_list["itemListElement"])
        assert positions == [1, 2]

        breadcrumbs = graph["BreadcrumbList"]["itemListElement"]
        assert breadcrumbs == [
            {"@type": "ListItem", "position": 1, "name": "Awesome Python", "item": "https://awesome-python.com/"},
            {"@type": "ListItem", "position": 2, "name": "Widgets", "item": "https://awesome-python.com/categories/widgets/"},
        ]

    def test_category_json_ld_follows_page_order(self, tmp_path):
        readme = textwrap.dedent("""\
            # Awesome Python

            Intro.

            ## Projects

            **Tools**

            ## Widgets

            _Widget libraries._

            - [zeta](https://example.com/zeta) - Listed first.
            - [alpha](https://example.com/alpha) - Listed second.

            # Contributing

            Help!
        """)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        self._copy_real_templates(tmp_path)
        build(tmp_path)

        category_html = (tmp_path / "website" / "output" / "categories" / "widgets" / "index.html").read_text(encoding="utf-8")
        marker = '<script type="application/ld+json">'
        start = category_html.index(marker) + len(marker)
        data = json.loads(category_html[start : category_html.index("</script>", start)])
        collection = next(node for node in data["@graph"] if node["@type"] == "CollectionPage")
        items = collection["mainEntity"]["itemListElement"]
        assert [(item["position"], item["name"]) for item in items] == [(1, "zeta"), (2, "alpha")]

    def test_group_page_falls_back_to_default_description_in_json_ld(self, tmp_path):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            **AI & ML**

            ## Deep Learning

            - [dl1](https://example.com/dl1) - DL.

            # Contributing

            Done.
        """)
        self._copy_real_templates(tmp_path)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        build(tmp_path)

        group_html = (tmp_path / "website" / "output" / "categories" / "ai-ml" / "index.html").read_text(encoding="utf-8")
        marker = '<script type="application/ld+json">'
        start = group_html.index(marker) + len(marker)
        end = group_html.index("</script>", start)
        data = json.loads(group_html[start:end])

        graph = {node["@type"]: node for node in data["@graph"]}
        collection = graph["CollectionPage"]
        assert collection["name"] == "Python AI & ML Libraries"
        assert collection["@id"] == "https://awesome-python.com/categories/ai-ml/"
        assert collection["url"] == "https://awesome-python.com/categories/ai-ml/"
        assert collection["description"] == "Explore 1 curated Python project in AI & ML. Part of the Awesome Python list."

    def test_category_title_skips_libraries_after_plural_noun(self, tmp_path):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            **Web Development**

            ## Web Frameworks

            - [wf1](https://example.com/wf1) - WF.

            ## Web APIs

            - [api1](https://example.com/api1) - API.

            # Contributing

            Done.
        """)
        self._copy_real_templates(tmp_path)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        build(tmp_path)

        categories_dir = tmp_path / "website" / "output" / "categories"
        frameworks_html = (categories_dir / "web-frameworks" / "index.html").read_text(encoding="utf-8")
        apis_html = (categories_dir / "web-apis" / "index.html").read_text(encoding="utf-8")
        parser = HeadMetadataParser()
        parser.feed(frameworks_html)
        marker = '<script type="application/ld+json">'
        start = frameworks_html.index(marker) + len(marker)
        end = frameworks_html.index("</script>", start)
        graph = {node["@type"]: node for node in json.loads(frameworks_html[start:end])["@graph"]}

        assert parser.title.strip() == "Python Web Frameworks - Awesome Python"
        assert parser.meta_by_property["og:title"] == "Python Web Frameworks - Awesome Python"
        assert graph["CollectionPage"]["name"] == "Python Web Frameworks"
        assert "<title>Python Web APIs Libraries - Awesome Python</title>" in apis_html

    def test_category_title_does_not_repeat_leading_python(self):
        assert category_meta_title("Python Language") == "Python Language Libraries - Awesome Python"

    def test_build_creates_subcategory_pages(self, tmp_path):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            **Web**

            ## Web Frameworks

            - Synchronous

                - [django](https://example.com/django) - Sync framework.

            - Asynchronous

                - [fastapi](https://example.com/fastapi) - Async framework.

            # Contributing

            Done.
        """)
        self._copy_real_templates(tmp_path)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        build(tmp_path)

        site = tmp_path / "website" / "output"
        sync = (site / "categories" / "web-frameworks" / "synchronous" / "index.html").read_text(encoding="utf-8")
        async_ = (site / "categories" / "web-frameworks" / "asynchronous" / "index.html").read_text(encoding="utf-8")

        assert "django" in sync
        assert "fastapi" not in sync
        assert "fastapi" in async_
        assert "django" not in async_

    def test_subcategory_page_shows_breadcrumb(self, tmp_path):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            **Web**

            ## Web Frameworks

            - Synchronous

                - [django](https://example.com/django) - Sync.

            # Contributing

            Done.
        """)
        self._copy_real_templates(tmp_path)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        build(tmp_path)

        site = tmp_path / "website" / "output"
        sync = (site / "categories" / "web-frameworks" / "synchronous" / "index.html").read_text(encoding="utf-8")
        assert 'href="/categories/web-frameworks/"' in sync
        assert "Web Frameworks" in sync
        assert "<h1>Synchronous</h1>" in sync
        assert "category-breadcrumb" in sync

        parser = HeadMetadataParser()
        parser.feed(sync)
        assert parser.title.strip() == "Python Web Frameworks: Synchronous - Awesome Python"
        assert parser.meta_by_name["description"] == "The Synchronous picks in Awesome Python's Web Frameworks list: django."

        marker = '<script type="application/ld+json">'
        start = sync.index(marker) + len(marker)
        end = sync.index("</script>", start)
        graph = {node["@type"]: node for node in json.loads(sync[start:end])["@graph"]}
        assert graph["CollectionPage"]["name"] == "Python Web Frameworks: Synchronous"
        assert graph["BreadcrumbList"]["itemListElement"] == [
            {"@type": "ListItem", "position": 1, "name": "Awesome Python", "item": "https://awesome-python.com/"},
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Web Frameworks",
                "item": "https://awesome-python.com/categories/web-frameworks/",
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": "Synchronous",
                "item": "https://awesome-python.com/categories/web-frameworks/synchronous/",
            },
        ]

        parent = (site / "categories" / "web-frameworks" / "index.html").read_text(encoding="utf-8")
        assert "category-breadcrumb" not in parent

    def test_sponsorship_page_contains_json_ld(self, tmp_path):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            **Tools**

            ## Widgets

            - [w1](https://example.com/w1) - A widget.

            # Contributing

            Done.
        """)
        self._copy_real_templates(tmp_path)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        build(tmp_path)

        site = tmp_path / "website" / "output"
        html = (site / "sponsorship" / "index.html").read_text(encoding="utf-8")
        parser = HeadMetadataParser()
        parser.feed(html)

        assert parser.title.strip() == "Sponsor Awesome Python"
        assert parser.meta_by_name["description"] == (
            "Sponsorship for Awesome Python: tiers, audience, and how to get your product in front of professional Python developers evaluating tools for production use."
        )
        assert parser.links_by_rel["canonical"] == "https://awesome-python.com/sponsorship/"
        assert '<a href="/sponsorship/" class="hero-topbar-link">Sponsorship</a>' in html

        marker = '<script type="application/ld+json">'
        start = html.index(marker) + len(marker)
        end = html.index("</script>", start)
        graph = {node["@type"]: node for node in json.loads(html[start:end])["@graph"]}

        assert set(graph) == {"WebSite", "WebPage", "BreadcrumbList"}
        assert graph["WebPage"]["@id"] == "https://awesome-python.com/sponsorship/"
        assert graph["WebPage"]["url"] == "https://awesome-python.com/sponsorship/"
        assert graph["BreadcrumbList"]["itemListElement"] == [
            {"@type": "ListItem", "position": 1, "name": "Awesome Python", "item": "https://awesome-python.com/"},
            {"@type": "ListItem", "position": 2, "name": "Sponsorship", "item": "https://awesome-python.com/sponsorship/"},
        ]

    def test_build_creates_group_pages(self, tmp_path):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            **AI & ML**

            ## Deep Learning

            - [dl1](https://example.com/dl1) - DL.

            ## Machine Learning

            - [ml1](https://example.com/ml1) - ML.

            **Web Development**

            ## Web Frameworks

            - [wf1](https://example.com/wf1) - WF.

            # Contributing

            Done.
        """)
        self._copy_real_templates(tmp_path)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        build(tmp_path)

        site = tmp_path / "website" / "output"
        ai_ml = (site / "categories" / "ai-ml" / "index.html").read_text(encoding="utf-8")
        web_dev = (site / "categories" / "web-development" / "index.html").read_text(encoding="utf-8")

        assert "dl1" in ai_ml
        assert "ml1" in ai_ml
        assert "wf1" not in ai_ml
        assert "wf1" in web_dev
        assert "dl1" not in web_dev

    def test_tags_link_to_pages_and_subcategory_anchors(self, tmp_path):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            **AI & ML**

            ## Deep Learning

            - Vision

                - [v1](https://example.com/v1) - Vision lib.

            # Contributing

            Done.
        """)
        self._copy_real_templates(tmp_path)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        build(tmp_path)

        site = tmp_path / "website" / "output"
        index_html = (site / "index.html").read_text(encoding="utf-8")

        category_html = (site / "categories" / "deep-learning" / "index.html").read_text(encoding="utf-8")

        for html in (index_html, category_html):
            assert 'href="/categories/deep-learning/#vision"' in html
            assert 'href="/categories/ai-ml/"' in html
            assert "data-url=" not in html
        assert 'href="/categories/deep-learning/"' in index_html
        assert 'id="vision"' in category_html

    _REDIRECT_README = textwrap.dedent("""\
        # Awesome Python

        Intro.

        ## Projects

        **Tools**

        ### Widgets

        - [w1](https://example.com/w1) - A widget.

        ## Contributing

        Help!
    """)

    def _write_redirects(self, tmp_path, redirects):
        data_dir = tmp_path / "website" / "data"
        data_dir.mkdir(parents=True)
        (data_dir / "redirects.json").write_text(json.dumps(redirects), encoding="utf-8")

    def test_build_writes_redirect_stub_outside_sitemap(self, tmp_path):
        self._copy_real_templates(tmp_path)
        (tmp_path / "README.md").write_text(self._REDIRECT_README, encoding="utf-8")
        self._write_redirects(tmp_path, {"/categories/old-widgets/": "/categories/widgets/"})
        build(tmp_path)

        site = tmp_path / "website" / "output"
        stub = (site / "categories" / "old-widgets" / "index.html").read_text(encoding="utf-8")
        assert '<link rel="canonical" href="https://awesome-python.com/categories/widgets/">' in stub
        assert '<meta http-equiv="refresh" content="0; url=https://awesome-python.com/categories/widgets/">' in stub
        assert "noindex" not in stub
        assert "old-widgets" not in (site / "sitemap.xml").read_text(encoding="utf-8")

    def test_build_renders_category_intro_and_uses_lead_as_meta_description(self, tmp_path):
        self._copy_real_templates(tmp_path)
        (tmp_path / "README.md").write_text(self._REDIRECT_README, encoding="utf-8")
        intros_dir = tmp_path / "website" / "data" / "category_intros"
        intros_dir.mkdir(parents=True)
        (intros_dir / "widgets.md").write_text("Use `w1` for most apps.\n\nSee [the docs](https://example.com/docs).\n\nHow to choose:\n\n- Small apps: w1\n", encoding="utf-8")
        build(tmp_path)

        category_html = (tmp_path / "website" / "output" / "categories" / "widgets" / "index.html").read_text(encoding="utf-8")
        parser = HeadMetadataParser()
        parser.feed(category_html)
        assert parser.meta_by_name["description"] == "Use w1 for most apps."
        assert '<div class="category-intro"><p>Use <code>w1</code> for most apps.</p>' in category_html
        assert '<li>Small apps: <a href="#entry-w1">w1</a></li>' in category_html
        assert '<a href="https://example.com/docs" target="_blank" rel="noopener">the docs</a>' in category_html

    def test_build_renders_category_guide_below_table(self, tmp_path):
        self._copy_real_templates(tmp_path)
        (tmp_path / "README.md").write_text(self._REDIRECT_README, encoding="utf-8")
        intros_dir = tmp_path / "website" / "data" / "category_intros"
        intros_dir.mkdir(parents=True)
        (intros_dir / "widgets.md").write_text("Use w1.\n\nHow to choose:\n\n- Small apps: w1\n\nSet up w1 once per process.\n", encoding="utf-8")
        build(tmp_path)

        category_html = (tmp_path / "website" / "output" / "categories" / "widgets" / "index.html").read_text(encoding="utf-8")
        intro_html = category_html.split('<div class="category-intro">', 1)[1].split("</div>", 1)[0]
        assert '<li>Small apps: <a href="#entry-w1">w1</a></li>' in intro_html
        assert "Set up w1" not in intro_html
        guide_html = category_html.split('<section class="guide-band" id="guide">', 1)[1]
        assert "<h2>Widgets guide</h2>" in guide_html
        assert "<p>Set up w1 once per process.</p>" in guide_html
        assert category_html.index('id="guide"') > category_html.index("</table>")
        assert '<a class="jump-link" href="#guide">Widgets guide</a>' in category_html

    def test_section_page_groups_rows_by_use_case_in_readme_order(self, tmp_path):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            **Tools**

            ### Widgets

            - Small
              - [w2](https://example.com/w2) - Second.
              - [w1](https://example.com/w1) - First.
            - Large
              - [w3](https://example.com/w3) - Third.
              - [sqlite3](https://docs.python.org/3/library/sqlite3.html) - Stdlib.

            # Contributing

            Done.
        """)
        self._copy_real_templates(tmp_path)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        build(tmp_path)

        site = tmp_path / "website" / "output" / "categories"
        html = (site / "widgets" / "index.html").read_text(encoding="utf-8")
        assert 'data-default-sort="editorial"' in html
        positions = [html.index(marker) for marker in ('<h2 id="small">', ">w2</a", ">w1</a", '<h2 id="large">', ">w3</a")]
        assert positions == sorted(positions)
        assert '<a class="jump-link" href="#small">Small</a>' in html
        assert '<a href="/categories/widgets/small/">Small</a>' in html
        assert '<a class="tag repeats-heading" href="/categories/widgets/#small">' in html
        assert '<tr class="desc-row">' in html

        subcategory_html = (site / "widgets" / "small" / "index.html").read_text(encoding="utf-8")
        assert 'data-default-sort="editorial"' in subcategory_html
        assert "group-row" not in subcategory_html
        assert subcategory_html.index(">w2</a") < subcategory_html.index(">w1</a")

        builtin_html = (site / "built-in" / "index.html").read_text(encoding="utf-8")
        assert "data-default-sort" not in builtin_html
        assert "group-row" not in builtin_html

    def test_group_page_groups_rows_by_section_with_links(self, tmp_path):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            **AI & ML**

            ## Machine Learning

            - [ml1](https://example.com/ml1) - ML.

            ## Deep Learning

            - [dl1](https://example.com/dl1) - DL.
            - [ml1](https://example.com/ml1) - ML again.

            # Contributing

            Done.
        """)
        self._copy_real_templates(tmp_path)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        build(tmp_path)

        html = (tmp_path / "website" / "output" / "categories" / "ai-ml" / "index.html").read_text(encoding="utf-8")
        assert 'data-default-sort="editorial"' in html
        ml_heading = html.index('<a href="/categories/machine-learning/">Machine Learning</a>')
        dl_heading = html.index('<a href="/categories/deep-learning/">Deep Learning</a>')
        assert ml_heading < html.index(">ml1</a") < dl_heading < html.index(">dl1</a")
        assert html.count(">ml1</a") == 1
        assert "repeats-heading" not in html
        assert 'class="jump-links"' not in html

    def test_group_page_shows_section_intro_lead_under_section_heading(self, tmp_path):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            **AI & ML**

            ## Machine Learning

            - [ml1](https://example.com/ml1) - ML.

            ## Deep Learning

            - [dl1](https://example.com/dl1) - DL.

            # Contributing

            Done.
        """)
        self._copy_real_templates(tmp_path)
        (tmp_path / "README.md").write_text(readme, encoding="utf-8")
        intros_dir = tmp_path / "website" / "data" / "category_intros"
        intros_dir.mkdir(parents=True)
        (intros_dir / "machine-learning.md").write_text("Start with [`ml1`](https://example.com/ml1).\n\nMore detail.\n", encoding="utf-8")
        build(tmp_path)

        html = (tmp_path / "website" / "output" / "categories" / "ai-ml" / "index.html").read_text(encoding="utf-8")
        lead = html.index('<div class="group-lead"><p>Start with <a href="https://example.com/ml1" target="_blank" rel="noopener"><code>ml1</code></a>.</p>')
        assert html.index('<a href="/categories/machine-learning/">Machine Learning</a>') < lead < html.index(">ml1</a")
        assert "More detail." not in html
        assert html.count('class="group-lead"') == 1

    def test_build_rejects_redirect_to_missing_page(self, tmp_path):
        self._copy_real_templates(tmp_path)
        (tmp_path / "README.md").write_text(self._REDIRECT_README, encoding="utf-8")
        self._write_redirects(tmp_path, {"/categories/old-widgets/": "/categories/gone/"})
        with pytest.raises(ValueError, match="does not exist"):
            build(tmp_path)

    def test_build_rejects_redirect_over_live_page(self, tmp_path):
        self._copy_real_templates(tmp_path)
        (tmp_path / "README.md").write_text(self._REDIRECT_README, encoding="utf-8")
        self._write_redirects(tmp_path, {"/categories/widgets/": "/"})
        with pytest.raises(ValueError, match="is a live page"):
            build(tmp_path)


# ---------------------------------------------------------------------------
# extract_github_repo
# ---------------------------------------------------------------------------


class TestExtractGithubRepo:
    def test_github_url(self):
        assert extract_github_repo("https://github.com/psf/requests") == "psf/requests"

    def test_non_github_url(self):
        assert extract_github_repo("https://foss.heptapod.net/pypy/pypy") is None

    def test_github_io_url(self):
        assert extract_github_repo("https://user.github.io/proj") is None

    def test_trailing_slash(self):
        assert extract_github_repo("https://github.com/org/repo/") == "org/repo"

    def test_deep_path(self):
        assert extract_github_repo("https://github.com/org/repo/tree/main") is None

    def test_dot_git_suffix(self):
        assert extract_github_repo("https://github.com/org/repo.git") == "org/repo"

    def test_org_only(self):
        assert extract_github_repo("https://github.com/org") is None


# ---------------------------------------------------------------------------
# sponsor_website_url
# ---------------------------------------------------------------------------


class TestSponsorWebsiteUrl:
    def test_replaces_readme_utm_content(self):
        url = "https://example.com?utm_source=awesome-python&utm_medium=sponsorship&utm_campaign=sponsor&utm_content=readme"
        assert sponsor_website_url(url) == "https://example.com?utm_source=awesome-python&utm_medium=sponsorship&utm_campaign=sponsor&utm_content=website"

    def test_keeps_path_and_other_params(self):
        assert sponsor_website_url("https://example.com/landing?ref=x&utm_content=readme") == "https://example.com/landing?ref=x&utm_content=website"

    def test_leaves_untagged_url_unchanged(self):
        assert sponsor_website_url("https://example.com") == "https://example.com"


# ---------------------------------------------------------------------------
# load_stars
# ---------------------------------------------------------------------------


class TestLoadStars:
    def test_returns_empty_when_missing(self, tmp_path):
        result = load_stars(tmp_path / "nonexistent.json")
        assert result == {}

    def test_loads_valid_json(self, tmp_path):
        data = {"psf/requests": {"stars": 52467, "owner": "psf", "fetched_at": "2026-01-01T00:00:00+00:00"}}
        f = tmp_path / "stars.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        result = load_stars(f)
        assert result["psf/requests"]["stars"] == 52467

    def test_returns_empty_on_corrupt_json(self, tmp_path):
        f = tmp_path / "stars.json"
        f.write_text("not json", encoding="utf-8")
        result = load_stars(f)
        assert result == {}


# ---------------------------------------------------------------------------
# sort_entries
# ---------------------------------------------------------------------------


class TestLoadPypiBadges:
    def test_only_entries_with_a_badge_are_returned(self):
        badges = load_pypi_badges()
        assert badges["azure-sdk-for-python"] == "Multiple on PyPI"
        assert badges["google-cloud-python"] == "Multiple on PyPI"
        # Entries whose missing count needs no explaining stay off the map
        assert "cpython" not in badges
        assert "tomllib" not in badges


def _template_entry(name: str, stars: int | None, source_type: str | None = None) -> TemplateEntry:
    return TemplateEntry(
        name=name,
        url="",
        description="",
        categories=[],
        groups=[],
        subcategories=[],
        stars=stars,
        downloads=None,
        owner=None,
        last_commit_at=None,
        source_type=source_type,
        bundled=False,
        badge=None,
        also_see=[],
    )


class TestSortEntries:
    def test_sorts_by_stars_descending(self):
        entries = [
            _template_entry("a", 100),
            _template_entry("b", 500),
            _template_entry("c", 200),
        ]
        result = sort_entries(entries)
        assert [e["name"] for e in result] == ["b", "c", "a"]

    def test_equal_stars_sorted_alphabetically(self):
        entries = [
            _template_entry("beta", 100),
            _template_entry("alpha", 100),
        ]
        result = sort_entries(entries)
        assert [e["name"] for e in result] == ["alpha", "beta"]

    def test_no_stars_go_to_bottom(self):
        entries = [
            _template_entry("no-stars", None),
            _template_entry("has-stars", 50),
        ]
        result = sort_entries(entries)
        assert [e["name"] for e in result] == ["has-stars", "no-stars"]

    def test_no_stars_sorted_alphabetically(self):
        entries = [
            _template_entry("zebra", None),
            _template_entry("apple", None),
        ]
        result = sort_entries(entries)
        assert [e["name"] for e in result] == ["apple", "zebra"]

    def test_builtin_between_starred_and_unstarred(self):
        entries = [
            _template_entry("builtin", None, "Stdlib"),
            _template_entry("starred", 100),
            _template_entry("unstarred", None),
        ]
        result = sort_entries(entries)
        assert [e["name"] for e in result] == ["starred", "builtin", "unstarred"]


# ---------------------------------------------------------------------------
# detect_source_type
# ---------------------------------------------------------------------------


class TestDetectSourceType:
    def test_github_repo_returns_none(self):
        assert detect_source_type("https://github.com/psf/requests") is None

    def test_stdlib_url(self):
        assert detect_source_type("https://docs.python.org/3/library/asyncio.html") == "Stdlib"

    def test_gitlab_url(self):
        assert detect_source_type("https://gitlab.com/org/repo") == "GitLab"

    def test_bitbucket_url(self):
        assert detect_source_type("https://bitbucket.org/org/repo") == "Bitbucket"

    def test_non_github_external(self):
        assert detect_source_type("https://example.com/tool") == "External"

    def test_github_non_repo_returns_none(self):
        assert detect_source_type("https://github.com/org/repo/wiki") is None


# ---------------------------------------------------------------------------
# extract_entries
# ---------------------------------------------------------------------------


class TestExtractEntries:
    def test_basic_extraction(self):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            **Tools**

            ## Widgets

            - [widget](https://example.com) - A widget.

            # Contributing

            Done.
        """)
        groups = parse_readme(readme)
        categories = [c for g in groups for c in g["categories"]]
        entries = extract_entries(categories, groups)
        assert len(entries) == 1
        assert entries[0]["name"] == "widget"
        assert entries[0]["categories"] == ["Widgets"]
        assert entries[0]["groups"] == ["Tools"]

    def test_duplicate_entry_merged(self):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            **Tools**

            ## Alpha

            - [shared](https://example.com/shared) - Shared lib.

            ## Beta

            - [shared](https://example.com/shared) - Shared lib.

            # Contributing

            Done.
        """)
        groups = parse_readme(readme)
        categories = [c for g in groups for c in g["categories"]]
        entries = extract_entries(categories, groups)
        shared = [e for e in entries if e["name"] == "shared"]
        assert len(shared) == 1
        assert sorted(shared[0]["categories"]) == ["Alpha", "Beta"]

    def test_source_type_detected(self):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            ## Stdlib

            - [asyncio](https://docs.python.org/3/library/asyncio.html) - Async I/O.

            # Contributing

            Done.
        """)
        groups = parse_readme(readme)
        categories = [c for g in groups for c in g["categories"]]
        entries = extract_entries(categories, groups)
        assert entries[0]["source_type"] == "Stdlib"

    def test_subcategory_includes_slug_and_url(self):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            **Tools**

            ## Web Frameworks

            - Synchronous

                - [django](https://example.com/django) - A framework.

            # Contributing

            Done.
        """)
        groups = parse_readme(readme)
        categories = [c for g in groups for c in g["categories"]]
        entries = extract_entries(categories, groups)
        assert entries[0]["subcategories"] == [
            {
                "name": "Synchronous",
                "value": "Web Frameworks > Synchronous",
                "slug": "synchronous",
                "url": "/categories/web-frameworks/synchronous/",
            },
        ]


# ---------------------------------------------------------------------------
# annotate_entries_with_stats
# ---------------------------------------------------------------------------


class TestAnnotateEntriesWithStats:
    def test_appends_star_count_to_bullet(self):
        markdown = "- [foo](https://github.com/owner/foo) - A foo.\n"
        stars = {"owner/foo": {"stars": 123, "owner": "owner"}}
        assert annotate_entries_with_stats(markdown, stars, {}) == ("- [foo](https://github.com/owner/foo) - A foo. (GitHub stars: 123)\n")

    def test_appends_downloads_by_display_name(self):
        markdown = "- [Foo.py](https://example.com) - A foo.\n"
        assert annotate_entries_with_stats(markdown, {}, {"foo-py": 777}) == ("- [Foo.py](https://example.com) - A foo. (PyPI downloads/month: 777)\n")

    def test_appends_downloads_and_stars_together(self):
        markdown = "- [foo](https://github.com/owner/foo) - A foo.\n"
        stars = {"owner/foo": {"stars": 123, "owner": "owner"}}
        assert annotate_entries_with_stats(markdown, stars, {"foo": 777}) == ("- [foo](https://github.com/owner/foo) - A foo. (PyPI downloads/month: 777, GitHub stars: 123)\n")

    def test_uses_first_github_link(self):
        markdown = "- [foo](https://github.com/owner/foo) - A foo. Also [bar](https://github.com/owner/bar).\n"
        stars = {
            "owner/foo": {"stars": 10, "owner": "owner"},
            "owner/bar": {"stars": 99, "owner": "owner"},
        }
        assert annotate_entries_with_stats(markdown, stars, {}) == ("- [foo](https://github.com/owner/foo) - A foo. Also [bar](https://github.com/owner/bar). (GitHub stars: 10)\n")

    def test_skips_entries_without_data(self):
        markdown = "- [foo](https://github.com/owner/foo) - A foo.\n"
        assert annotate_entries_with_stats(markdown, {}, {}) == markdown

    def test_skips_non_github_links_for_stars(self):
        markdown = "- [foo](https://example.com) - A foo.\n"
        stars = {"owner/foo": {"stars": 1, "owner": "owner"}}
        assert annotate_entries_with_stats(markdown, stars, {}) == markdown

    def test_skips_non_bullet_lines(self):
        markdown = "See [foo](https://github.com/owner/foo) for details.\n"
        stars = {"owner/foo": {"stars": 1, "owner": "owner"}}
        assert annotate_entries_with_stats(markdown, stars, {"foo": 5}) == markdown

    def test_handles_indented_bullets(self):
        markdown = "    - [foo](https://github.com/owner/foo)\n"
        stars = {"owner/foo": {"stars": 7, "owner": "owner"}}
        assert annotate_entries_with_stats(markdown, stars, {}) == ("    - [foo](https://github.com/owner/foo) (GitHub stars: 7)\n")

    def test_preserves_lines_without_trailing_newline(self):
        markdown = "- [foo](https://github.com/owner/foo) - A foo."
        stars = {"owner/foo": {"stars": 5, "owner": "owner"}}
        assert annotate_entries_with_stats(markdown, stars, {}) == ("- [foo](https://github.com/owner/foo) - A foo. (GitHub stars: 5)")


class TestLoadDownloads:
    def test_parses_tsv_and_skips_not_found(self, tmp_path):
        tsv = tmp_path / "pypi_downloads.tsv"
        tsv.write_text(
            "name\tpackage\tdownloads\tfetched_at\naiohttp\taiohttp\t649105404\t2026-08-16\npytorch\ttorch\t50000000\t2026-08-16\ndead-pkg\t-\tNOT_FOUND\t2026-08-16\n",
            encoding="utf-8",
        )
        assert load_downloads(tsv) == {"aiohttp": 649105404, "pytorch": 50000000}

    def test_missing_file_returns_empty(self, tmp_path):
        assert load_downloads(tmp_path / "nope.tsv") == {}


# ---------------------------------------------------------------------------
# load_category_intro
# ---------------------------------------------------------------------------


class TestLoadCategoryIntro:
    def test_splits_after_how_to_choose_list(self, tmp_path):
        path = tmp_path / "widgets.md"
        path.write_text("Use `w1` for most apps.\n\nHow to choose:\n\n- Small apps: w1\n- Big apps: w2\n\nConfigure w1 once.\n\nPin w2.\n", encoding="utf-8")
        intro_html, guide_html, lead, lead_html = load_category_intro(path)
        assert intro_html == "<p>Use <code>w1</code> for most apps.</p>\n<p>How to choose:</p>\n<ul>\n<li>Small apps: w1</li>\n<li>Big apps: w2</li>\n</ul>\n"
        assert guide_html == "<p>Configure w1 once.</p>\n<p>Pin w2.</p>\n"
        assert lead == "Use w1 for most apps."
        assert lead_html == "<p>Use <code>w1</code> for most apps.</p>\n"

    def test_splits_after_lead_without_how_to_choose_list(self, tmp_path):
        path = tmp_path / "widgets.md"
        path.write_text("Use w1.\n\n- Small apps: w1\n\nConfigure w1 once.\n", encoding="utf-8")
        intro_html, guide_html, _, _ = load_category_intro(path)
        assert intro_html == "<p>Use w1.</p>\n"
        assert guide_html == "<ul>\n<li>Small apps: w1</li>\n</ul>\n<p>Configure w1 once.</p>\n"

    def test_returns_empty_strings_without_intro_file(self, tmp_path):
        assert load_category_intro(tmp_path / "missing.md") == ("", "", "", "")

    def test_links_picks_to_entry_rows(self, tmp_path):
        path = tmp_path / "widgets.md"
        path.write_text(
            "Use w1.\n\nHow to choose:\n\n- Small apps: Django Ninja, or `uv tool` on uv\n- Big apps: Django\n- Old apps: Django - LTS releases\n\nSee [w1](https://w1.example).\n", encoding="utf-8"
        )
        intro_html, guide_html, _, _ = load_category_intro(path, ["django-ninja", "Django", "uv"])
        assert '<li>Small apps: <a href="#entry-django-ninja">Django Ninja</a>, or <code>uv tool</code> on <a href="#entry-uv">uv</a></li>' in intro_html
        assert '<li>Big apps: <a href="#entry-django">Django</a></li>' in intro_html
        assert '<li>Old apps: <a href="#entry-django">Django</a> - LTS releases</li>' in intro_html
        assert '<a href="https://w1.example" target="_blank" rel="noopener">w1</a>' in guide_html

    def test_links_pick_aliases_to_entry_rows(self, tmp_path):
        path = tmp_path / "widgets.md"
        path.write_text("Use w1.\n\nHow to choose:\n\n- Vision: OpenCV\n", encoding="utf-8")
        intro_html, _, _, _ = load_category_intro(path, ["opencv-python"])
        assert '<li>Vision: <a href="#entry-opencv-python">OpenCV</a></li>' in intro_html



================================================
FILE: website/tests/test_fetch_github_stars.py
================================================
"""Tests for fetch_github_stars module."""

import json
from datetime import UTC

from fetch_github_stars import (
    build_graphql_query,
    extract_github_repos,
    parse_graphql_response,
    save_cache,
)


class TestExtractGithubRepos:
    def test_extracts_owner_repo_from_github_url(self):
        readme = "* [requests](https://github.com/psf/requests) - HTTP lib."
        result = extract_github_repos(readme)
        assert result == {"psf/requests"}

    def test_multiple_repos(self):
        readme = "* [requests](https://github.com/psf/requests) - HTTP.\n* [flask](https://github.com/pallets/flask) - Micro."
        result = extract_github_repos(readme)
        assert result == {"psf/requests", "pallets/flask"}

    def test_deduplicates(self):
        readme = "* [a](https://github.com/org/repo) - A.\n* [b](https://github.com/org/repo) - B."
        result = extract_github_repos(readme)
        assert result == {"org/repo"}

    def test_strips_fragment(self):
        readme = "* [lib](https://github.com/org/repo#section) - Lib."
        result = extract_github_repos(readme)
        assert result == {"org/repo"}


class TestSaveCache:
    def test_creates_directory_and_writes_json(self, tmp_path, monkeypatch):
        data_dir = tmp_path / "data"
        cache_file = data_dir / "stars.json"
        monkeypatch.setattr("fetch_github_stars.DATA_DIR", data_dir)
        monkeypatch.setattr("fetch_github_stars.CACHE_FILE", cache_file)
        save_cache({"a/b": {"stars": 1}})
        assert cache_file.exists()
        assert json.loads(cache_file.read_text(encoding="utf-8")) == {"a/b": {"stars": 1}}


class TestBuildGraphqlQuery:
    def test_single_repo(self):
        query = build_graphql_query(["psf/requests"])
        assert "repository" in query
        assert 'owner: "psf"' in query
        assert 'name: "requests"' in query
        assert "stargazerCount" in query

    def test_multiple_repos_use_aliases(self):
        query = build_graphql_query(["psf/requests", "pallets/flask"])
        assert "repo_0:" in query
        assert "repo_1:" in query

    def test_empty_list(self):
        query = build_graphql_query([])
        assert query == ""

    def test_skips_repos_with_quotes_in_name(self):
        query = build_graphql_query(['org/"bad"'])
        assert query == ""

    def test_skips_only_bad_repos(self):
        query = build_graphql_query(["good/repo", 'bad/"repo"'])
        assert "good" in query
        assert "bad" not in query

    def test_skips_graphql_injection_in_owner(self):
        query = build_graphql_query(['org"){evil}/repo'])
        assert query == ""

    def test_skips_graphql_injection_in_name(self):
        query = build_graphql_query(['org/repo"){evil}'])
        assert query == ""

    def test_skips_owner_starting_with_hyphen(self):
        query = build_graphql_query(["-bad/repo"])
        assert query == ""

    def test_skips_owner_starting_with_dot(self):
        query = build_graphql_query([".bad/repo"])
        assert query == ""

    def test_skips_repo_starting_with_dot(self):
        query = build_graphql_query(["org/.hidden"])
        assert query == ""

    def test_allows_repo_with_dots_and_underscores(self):
        query = build_graphql_query(["org/my_repo.py"])
        assert 'name: "my_repo.py"' in query

    def test_allows_hyphenated_owner(self):
        query = build_graphql_query(["my-org/repo"])
        assert 'owner: "my-org"' in query

    def test_skips_owner_with_underscore(self):
        query = build_graphql_query(["bad_owner/repo"])
        assert query == ""


class TestParseGraphqlResponse:
    def test_parses_star_count_and_owner(self):
        data = {
            "repo_0": {
                "stargazerCount": 52467,
                "owner": {"login": "psf"},
            }
        }
        repos = ["psf/requests"]
        result = parse_graphql_response(data, repos)
        assert result["psf/requests"]["stars"] == 52467
        assert result["psf/requests"]["owner"] == "psf"

    def test_skips_null_repos(self):
        data = {"repo_0": None}
        repos = ["deleted/repo"]
        result = parse_graphql_response(data, repos)
        assert result == {}

    def test_handles_missing_owner(self):
        data = {"repo_0": {"stargazerCount": 100}}
        repos = ["org/repo"]
        result = parse_graphql_response(data, repos)
        assert result["org/repo"]["owner"] == ""

    def test_multiple_repos(self):
        data = {
            "repo_0": {"stargazerCount": 100, "owner": {"login": "a"}},
            "repo_1": {"stargazerCount": 200, "owner": {"login": "b"}},
        }
        repos = ["a/x", "b/y"]
        result = parse_graphql_response(data, repos)
        assert len(result) == 2
        assert result["a/x"]["stars"] == 100
        assert result["b/y"]["stars"] == 200

    def test_extracts_last_commit_at(self):
        data = {
            "repo_0": {
                "stargazerCount": 100,
                "owner": {"login": "org"},
                "defaultBranchRef": {"target": {"committedDate": "2025-06-01T00:00:00Z"}},
            }
        }
        repos = ["org/repo"]
        result = parse_graphql_response(data, repos)
        assert result["org/repo"]["last_commit_at"] == "2025-06-01T00:00:00Z"

    def test_missing_default_branch_ref(self):
        data = {"repo_0": {"stargazerCount": 50, "owner": {"login": "org"}}}
        repos = ["org/repo"]
        result = parse_graphql_response(data, repos)
        assert result["org/repo"]["last_commit_at"] == ""


class TestMainSkipsFreshCache:
    """Verify that main() skips fetching when all cache entries are fresh."""

    def test_skips_fetch_when_cache_is_fresh(self, tmp_path, monkeypatch, capsys):
        from datetime import datetime, timedelta

        from fetch_github_stars import main

        # Set up a minimal README with one repo
        readme = tmp_path / "README.md"
        readme.write_text("* [req](https://github.com/psf/requests) - HTTP.\n")
        monkeypatch.setattr("fetch_github_stars.README_PATH", readme)

        # Pre-populate cache with a fresh entry (1 hour ago)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        cache_file = data_dir / "github_stars.json"
        now = datetime.now(UTC)
        fresh_cache = {
            "psf/requests": {
                "stars": 52000,
                "owner": "psf",
                "last_commit_at": "2025-01-01T00:00:00+00:00",
                "fetched_at": (now - timedelta(hours=1)).isoformat(),
            },
            "vinta/awesome-python": {
                "stars": 230000,
                "owner": "vinta",
                "last_commit_at": "2025-01-01T00:00:00+00:00",
                "fetched_at": (now - timedelta(hours=1)).isoformat(),
            },
        }
        cache_file.write_text(json.dumps(fresh_cache), encoding="utf-8")
        monkeypatch.setattr("fetch_github_stars.CACHE_FILE", cache_file)
        monkeypatch.setattr("fetch_github_stars.DATA_DIR", data_dir)
        monkeypatch.setenv("GITHUB_TOKEN", "fake-token")

        main()

        output = capsys.readouterr().out
        assert "0 repos to fetch" in output
        assert "Cache is up to date" in output

    def test_fetches_when_cache_is_stale(self, tmp_path, monkeypatch, capsys):
        from datetime import datetime, timedelta
        from unittest.mock import MagicMock

        from fetch_github_stars import main

        # Set up a minimal README with one repo
        readme = tmp_path / "README.md"
        readme.write_text("* [req](https://github.com/psf/requests) - HTTP.\n")
        monkeypatch.setattr("fetch_github_stars.README_PATH", readme)

        # Pre-populate cache with a stale entry (24 hours ago)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        cache_file = data_dir / "github_stars.json"
        now = datetime.now(UTC)
        stale_cache = {
            "psf/requests": {
                "stars": 52000,
                "owner": "psf",
                "last_commit_at": "2025-01-01T00:00:00+00:00",
                "fetched_at": (now - timedelta(hours=24)).isoformat(),
            },
            "vinta/awesome-python": {
                "stars": 230000,
                "owner": "vinta",
                "last_commit_at": "2025-01-01T00:00:00+00:00",
                "fetched_at": (now - timedelta(hours=24)).isoformat(),
            },
        }
        cache_file.write_text(json.dumps(stale_cache), encoding="utf-8")
        monkeypatch.setattr("fetch_github_stars.CACHE_FILE", cache_file)
        monkeypatch.setattr("fetch_github_stars.DATA_DIR", data_dir)
        monkeypatch.setenv("GITHUB_TOKEN", "fake-token")

        # Mock httpx.Client to avoid real API calls
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "repo_0": {
                    "stargazerCount": 53000,
                    "owner": {"login": "psf"},
                    "defaultBranchRef": {"target": {"committedDate": "2025-06-01T00:00:00Z"}},
                },
                "repo_1": {
                    "stargazerCount": 231000,
                    "owner": {"login": "vinta"},
                    "defaultBranchRef": {"target": {"committedDate": "2025-06-01T00:00:00Z"}},
                },
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response
        monkeypatch.setattr("fetch_github_stars.httpx.Client", lambda **kwargs: mock_client)

        main()

        output = capsys.readouterr().out
        assert "2 repos to fetch" in output
        assert "Done. Fetched 2 repos" in output
        mock_client.post.assert_called_once()



================================================
FILE: website/tests/test_preview_verdicts.py
================================================
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

TEMPLATE = Path(__file__).resolve().parents[2] / ".claude/skills/preview-verdicts/template.html"
NODE = shutil.which("node")

RUNNER = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const { script, actions } = JSON.parse(fs.readFileSync(0, "utf8"));
const storage = {};
let elements, context, copied;
function reload() {
  elements = {};
  context = vm.createContext({
    document: { getElementById: id => elements[id] ||= {}, title: "Review" },
    localStorage: { getItem: key => storage[key], setItem: (key, value) => storage[key] = value },
    navigator: { clipboard: { writeText: text => { copied = text; return Promise.resolve(); } } }
  });
  vm.runInContext(script, context);
}
function snapshot() {
  return {
    html: elements.app.innerHTML,
    counts: elements.counts.innerHTML,
    feedback: context.collect(),
    rowClass: elements["r-Section__entry"]?.className,
    copied
  };
}
reload();
const snapshots = [snapshot()];
for (const [action, ...args] of actions) {
  if (action === "reload") reload();
  else context[action](...args);
  snapshots.push(snapshot());
}
process.stdout.write(JSON.stringify(snapshots));
"""


def preview(kind, verdict, actions=(), source=None):
    if NODE is None:
        pytest.skip("Preview script tests require Node.js")
    row = ["entry", "https://github.com/owner/entry", "1,000", kind, verdict, "Review reason"]
    if source is not None:
        row.append(source)
    data = [["Section", "Use case — review note", [row]]]
    script = TEMPLATE.read_text().split("<script>", 1)[1].split("</script>", 1)[0].replace("__DATA__", json.dumps(data))
    result = subprocess.run([NODE, "-e", RUNNER], input=json.dumps({"script": script, "actions": actions}), capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


@pytest.mark.parametrize(
    ("kind", "accept", "reject", "buttons"),
    [
        ("listed", "keep", "remove", ["Keep", "Remove", "Park"]),
        ("candidate", "add", "reject", ["Add", "Reject", "Park"]),
        ("structure", "restructure", "reject", ["Restructure", "Park", "Reject"]),
    ],
)
def test_parked_rows_keep_their_choices_and_feedback_after_reload(kind, accept, reject, buttons):
    initial, accepted, reloaded, copied, rejected, parked = preview(
        kind,
        "park",
        [("setV", "Section::entry", accept), ("reload",), ("copyFeedback",), ("setV", "Section::entry", reject), ("setV", "Section::entry", "park")],
    )
    for snapshot in (initial, accepted, reloaded, copied, rejected, parked):
        assert re.findall(r"<button[^>]*>([^<]+)</button>", snapshot["html"]) == buttons
    assert initial["feedback"] == parked["feedback"] == []
    expected = [{"section": "Section", "subcategory": "Use case", "entry": "entry", "kind": kind, "my_verdict": "park", "your_verdict": accept, "reason": ""}]
    assert accepted["feedback"] == reloaded["feedback"] == expected
    assert json.loads(copied["copied"]) == expected
    assert rejected["feedback"][0]["your_verdict"] == reject
    assert f'<button class="{accept} on"' in reloaded["html"]
    assert "<b>1</b> verdicts flipped" in reloaded["counts"]
    assert "<b>0</b> verdicts flipped" in parked["counts"]


@pytest.mark.parametrize(("kind", "verdict"), [("listed", "keep"), ("listed", "remove"), ("candidate", "add"), ("candidate", "reject"), ("structure", "restructure"), ("structure", "reject")])
def test_existing_verdicts_can_be_parked_without_losing_kind(kind, verdict):
    initial, parked, reloaded = preview(kind, verdict, [("setV", "Section::entry", "park"), ("reload",)])
    assert initial["feedback"] == []
    assert f'<button class="{verdict} on"' in initial["html"]
    assert parked["feedback"] == reloaded["feedback"]
    assert reloaded["feedback"][0] == {"section": "Section", "subcategory": "Use case", "entry": "entry", "kind": kind, "my_verdict": verdict, "your_verdict": "park", "reason": ""}


def test_comment_only_feedback_preserves_parked_kind_and_clears_highlight():
    _, commented, cleared = preview("candidate", "park", [("setF", "Section::entry", "  Need evidence  "), ("setF", "Section::entry", "")])
    assert commented["feedback"][0] == {"section": "Section", "subcategory": "Use case", "entry": "entry", "kind": "candidate", "my_verdict": "park", "your_verdict": "park", "reason": "Need evidence"}
    assert commented["rowClass"] == "changed"
    assert cleared["rowClass"] == ""
    assert cleared["feedback"] == []


def test_source_column_uses_optional_seventh_field():
    without_source = preview("candidate", "add")[0]["html"]
    with_source = preview("candidate", "add", source="Starred engine")[0]["html"]
    assert "<th>Source</th>" not in without_source
    assert "Review reason" in without_source
    assert "<th>Source</th>" in with_source
    assert '<td class="source">Starred engine</td>' in with_source



================================================
FILE: website/tests/test_readme_parser.py
================================================
"""Tests for the readme_parser module."""

import re
import textwrap
from pathlib import Path

import pytest
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

from fetch_pypi_downloads_via_clickpy import PYPI_NAME_RE, load_overrides, normalize
from readme_parser import (
    _find_inline,
    _parse_section_entries,
    parse_readme,
    render_inline_html,
    render_inline_text,
)


def _parse_inline(md_text: str) -> list[SyntaxTreeNode]:
    """Helper: parse a single paragraph and return its inline children."""
    md = MarkdownIt("commonmark")
    root = SyntaxTreeNode(md.parse(md_text))
    # root > paragraph > inline > children
    return root.children[0].children[0].children


class TestRenderInlineHtml:
    def test_plain_text_escapes_html(self):
        children = _parse_inline("Hello <world> & friends")
        assert render_inline_html(children) == "Hello &lt;world&gt; &amp; friends"

    def test_link_with_target(self):
        children = _parse_inline("[name](https://example.com)")
        html = render_inline_html(children)
        assert 'href="https://example.com"' in html
        assert 'target="_blank"' in html
        assert 'rel="noopener"' in html
        assert ">name</a>" in html

    def test_emphasis(self):
        children = _parse_inline("*italic* text")
        assert "<em>italic</em>" in render_inline_html(children)

    def test_strong(self):
        children = _parse_inline("**bold** text")
        assert "<strong>bold</strong>" in render_inline_html(children)

    def test_code_inline(self):
        children = _parse_inline("`some code`")
        assert "<code>some code</code>" in render_inline_html(children)

    def test_mixed_link_and_text(self):
        children = _parse_inline("See [foo](https://x.com) for details.")
        html = render_inline_html(children)
        assert "See " in html
        assert ">foo</a>" in html
        assert " for details." in html


class TestRenderInlineText:
    def test_plain_text(self):
        children = _parse_inline("Hello world")
        assert render_inline_text(children) == "Hello world"

    def test_link_becomes_text(self):
        children = _parse_inline("See [awesome-algos](https://github.com/x/y).")
        assert render_inline_text(children) == "See awesome-algos."

    def test_emphasis_stripped(self):
        children = _parse_inline("*italic* text")
        assert render_inline_text(children) == "italic text"

    def test_code_inline_kept(self):
        children = _parse_inline("`code` here")
        assert render_inline_text(children) == "code here"


MINIMAL_README = textwrap.dedent("""\
    # Awesome Python

    Some intro text.

    ## Projects

    ### Alpha

    _Libraries for alpha stuff._

    - [lib-a](https://example.com/a) - Does A.
    - [lib-b](https://example.com/b) - Does B.

    ### Beta

    _Tools for beta._

    - [lib-c](https://example.com/c) - Does C.

    ## Resources

    Where to discover resources.

    ### Newsletters

    - [News One](https://example.com/n1)
    - [News Two](https://example.com/n2)

    ### Podcasts

    - [Pod One](https://example.com/p1)

    ## Contributing

    Please contribute!
""")


GROUPED_README = textwrap.dedent("""\
    # Awesome Python

    Some intro text.

    ## Projects

    **Group One**

    ### Alpha

    _Libraries for alpha stuff._

    - [lib-a](https://example.com/a) - Does A.
    - [lib-b](https://example.com/b) - Does B.

    **Group Two**

    ### Beta

    _Tools for beta._

    - [lib-c](https://example.com/c) - Does C.

    ### Gamma

    - [lib-d](https://example.com/d) - Does D.

    ## Resources

    Where to discover resources.

    ### Newsletters

    - [News One](https://example.com/n1)

    ## Contributing

    Please contribute!
""")


class TestParseReadmeSections:
    def test_ungrouped_categories_go_to_other(self):
        groups = parse_readme(MINIMAL_README)
        assert len(groups) == 1
        assert groups[0]["name"] == "Other"
        assert len(groups[0]["categories"]) == 2

    def test_ungrouped_category_names(self):
        groups = parse_readme(MINIMAL_README)
        cats = groups[0]["categories"]
        assert cats[0]["name"] == "Alpha"
        assert cats[1]["name"] == "Beta"

    def test_category_slugs(self):
        groups = parse_readme(MINIMAL_README)
        cats = groups[0]["categories"]
        assert cats[0]["slug"] == "alpha"
        assert cats[1]["slug"] == "beta"

    def test_category_description(self):
        groups = parse_readme(MINIMAL_README)
        cats = groups[0]["categories"]
        assert cats[0]["description"] == "Libraries for alpha stuff."
        assert cats[0]["description_html"] == "Libraries for alpha stuff."
        assert cats[1]["description"] == "Tools for beta."
        assert cats[1]["description_html"] == "Tools for beta."

    def test_contributing_skipped(self):
        groups = parse_readme(MINIMAL_README)
        all_names = []
        for g in groups:
            all_names.extend(c["name"] for c in g["categories"])
        assert "Contributing" not in all_names

    def test_no_projects_heading(self):
        groups = parse_readme("# Just a heading\n\nSome text.\n")
        assert groups == []

    def test_no_description(self):
        readme = textwrap.dedent("""\
            # Title

            ## Projects

            ### NullDesc

            - [item](https://x.com) - Thing.

            ## Resources

            ### Tips

            - [tip](https://x.com)

            ## Contributing

            Done.
        """)
        groups = parse_readme(readme)
        cats = groups[0]["categories"]
        assert cats[0]["description"] == ""
        assert cats[0]["description_html"] == ""
        assert cats[0]["entries"][0]["name"] == "item"

    def test_description_with_link_stripped(self):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            ### Algos

            _Algorithms. Also see [awesome-algos](https://example.com)._

            - [lib](https://x.com) - Lib.

            ## Contributing

            Done.
        """)
        groups = parse_readme(readme)
        cats = groups[0]["categories"]
        assert cats[0]["description"] == "Algorithms. Also see awesome-algos."
        assert cats[0]["description_html"] == 'Algorithms. Also see <a href="https://example.com" target="_blank" rel="noopener">awesome-algos</a>.'


class TestParseGroupedReadme:
    def test_group_count(self):
        groups = parse_readme(GROUPED_README)
        assert len(groups) == 2

    def test_group_names(self):
        groups = parse_readme(GROUPED_README)
        assert groups[0]["name"] == "Group One"
        assert groups[1]["name"] == "Group Two"

    def test_group_slugs(self):
        groups = parse_readme(GROUPED_README)
        assert groups[0]["slug"] == "group-one"
        assert groups[1]["slug"] == "group-two"

    def test_group_one_has_one_category(self):
        groups = parse_readme(GROUPED_README)
        assert len(groups[0]["categories"]) == 1
        assert groups[0]["categories"][0]["name"] == "Alpha"

    def test_group_two_has_two_categories(self):
        groups = parse_readme(GROUPED_README)
        assert len(groups[1]["categories"]) == 2
        assert groups[1]["categories"][0]["name"] == "Beta"
        assert groups[1]["categories"][1]["name"] == "Gamma"

    def test_empty_group_skipped(self):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            **Empty**

            **HasCats**

            ### Cat

            - [x](https://x.com) - X.

            ## Contributing

            Done.
        """)
        groups = parse_readme(readme)
        assert len(groups) == 1
        assert groups[0]["name"] == "HasCats"

    def test_bold_with_extra_text_not_group_marker(self):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            **Note:** This is not a group marker.

            ### Cat

            - [x](https://x.com) - X.

            ## Contributing

            Done.
        """)
        groups = parse_readme(readme)
        # "Note:" has text after the strong node, so it's not a group marker
        # Category goes into "Other"
        assert len(groups) == 1
        assert groups[0]["name"] == "Other"

    def test_categories_before_any_group_marker(self):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            ### Orphan

            - [x](https://x.com) - X.

            **A Group**

            ### Grouped

            - [y](https://x.com) - Y.

            ## Contributing

            Done.
        """)
        groups = parse_readme(readme)
        assert len(groups) == 2
        assert groups[0]["name"] == "Other"
        assert groups[0]["categories"][0]["name"] == "Orphan"
        assert groups[1]["name"] == "A Group"
        assert groups[1]["categories"][0]["name"] == "Grouped"


def _content_nodes(md_text: str) -> list[SyntaxTreeNode]:
    """Helper: parse markdown and return all block nodes."""
    md = MarkdownIt("commonmark")
    root = SyntaxTreeNode(md.parse(md_text))
    return root.children


class TestParseSectionEntries:
    def test_flat_entries(self):
        nodes = _content_nodes("- [django](https://example.com/d) - A web framework.\n- [flask](https://example.com/f) - A micro framework.\n")
        entries = _parse_section_entries(nodes)
        assert len(entries) == 2
        assert entries[0]["name"] == "django"
        assert entries[0]["url"] == "https://example.com/d"
        assert "web framework" in entries[0]["description"]
        assert entries[0]["also_see"] == []
        assert entries[1]["name"] == "flask"

    def test_link_only_entry(self):
        nodes = _content_nodes("- [tool](https://x.com)\n")
        entries = _parse_section_entries(nodes)
        assert len(entries) == 1
        assert entries[0]["name"] == "tool"
        assert entries[0]["description"] == ""

    def test_subcategorized_entries(self):
        nodes = _content_nodes("- Algorithms\n  - [algos](https://x.com/a) - Algo lib.\n  - [sorts](https://x.com/s) - Sort lib.\n- Design Patterns\n  - [patterns](https://x.com/p) - Pattern lib.\n")
        entries = _parse_section_entries(nodes)
        assert len(entries) == 3
        assert entries[0]["name"] == "algos"
        assert entries[2]["name"] == "patterns"

    def test_text_before_link_is_subcategory(self):
        nodes = _content_nodes(
            "- MySQL - [awesome-mysql](http://example.com/awesome-mysql/)\n"
            "  - [mysqlclient](https://example.com/mysqlclient) - MySQL connector.\n"
            "  - [pymysql](https://example.com/pymysql) - Pure Python MySQL driver.\n"
        )
        entries = _parse_section_entries(nodes)
        # awesome-mysql is a subcategory label, not an entry
        assert len(entries) == 2
        names = [e["name"] for e in entries]
        assert "awesome-mysql" not in names
        assert "mysqlclient" in names
        assert "pymysql" in names

    def test_also_see_sub_entries(self):
        nodes = _content_nodes(
            "- [asyncio](https://docs.python.org/3/library/asyncio.html) - Async I/O.\n"
            "  - [awesome-asyncio](https://github.com/timofurrer/awesome-asyncio)\n"
            "- [trio](https://github.com/python-trio/trio) - Friendly async.\n"
        )
        entries = _parse_section_entries(nodes)
        assert len(entries) == 2
        assert entries[0]["name"] == "asyncio"
        assert len(entries[0]["also_see"]) == 1
        assert entries[0]["also_see"][0]["name"] == "awesome-asyncio"
        assert entries[1]["name"] == "trio"
        assert entries[1]["also_see"] == []

    def test_entry_count_includes_also_see(self):
        readme = textwrap.dedent("""\
            # T

            ## Projects

            ### Async

            - [asyncio](https://x.com) - Async I/O.
              - [awesome-asyncio](https://y.com)
            - [trio](https://z.com) - Friendly async.

            ## Contributing

            Done.
        """)
        groups = parse_readme(readme)
        cats = groups[0]["categories"]
        # 2 main entries + 1 also_see = 3
        assert cats[0]["entry_count"] == 3

    def test_description_html_escapes_xss(self):
        nodes = _content_nodes("- [lib](https://x.com) - A <script>alert(1)</script> lib.\n")
        entries = _parse_section_entries(nodes)
        assert "<script>" not in entries[0]["description"]
        assert "&lt;script&gt;" in entries[0]["description"]


class TestParseRealReadme:
    @pytest.fixture(autouse=True)
    def load_readme(self):
        readme_path = Path(__file__).resolve().parents[2] / "README.md"
        self.readme_text = readme_path.read_text(encoding="utf-8")
        self.groups = parse_readme(self.readme_text)
        self.cats = [c for g in self.groups for c in g["categories"]]

    def test_at_least_11_groups(self):
        assert len(self.groups) >= 11

    def test_at_least_69_categories(self):
        assert len(self.cats) >= 69

    def test_contributing_not_in_results(self):
        all_names = [c["name"] for c in self.cats]
        assert "Contributing" not in all_names

    def test_entry_counts_nonzero(self):
        for cat in self.cats:
            assert cat["entry_count"] > 0, f"{cat['name']} has 0 entries"

    def test_all_entries_have_nonempty_names(self):
        bad = []
        for cat in self.cats:
            for entry in cat["entries"]:
                if not entry["name"].strip():
                    bad.append(f"{cat['name']}: empty entry name (url={entry['url']})")
        assert bad == [], "Entries with empty names:\n" + "\n".join(bad)

    def test_all_entries_have_valid_urls(self):
        bad = []
        for cat in self.cats:
            for entry in cat["entries"]:
                if not entry["url"].startswith(("https://", "http://")):
                    bad.append(f"{cat['name']}: [{entry['name']}] has invalid url: {entry['url']!r}")
                for see in entry["also_see"]:
                    if not see["url"].startswith(("https://", "http://")):
                        bad.append(f"{cat['name']}: [{see['name']}] (also_see) has invalid url: {see['url']!r}")
        assert bad == [], "Entries with invalid URLs:\n" + "\n".join(bad)

    def test_bundled_entries_are_never_queried_on_pypi(self):
        """A "(part of X)" entry ships inside something else, so it has no package of its own.

        If its display name happens to be PyPI-shaped and no null override
        records that, the download sweep queries PyPI and silently measures
        whatever unrelated project owns the name. That is how uv-audit picked
        up a third-party package after being renamed from "uv audit".
        """
        overrides = load_overrides()
        bad = []
        for cat in self.cats:
            for entry in cat["entries"]:
                if not re.match(r"^\(part of ", entry["description"]):
                    continue
                name = normalize(entry["name"])
                if PYPI_NAME_RE.match(name) and overrides.get(name, name) is not None:
                    bad.append(f"[{entry['name']}] needs a null entry in pypi_name_overrides.json")
        assert bad == [], "Bundled entries the download sweep would query:\n" + "\n".join(bad)

    def test_no_malformed_entry_lines(self):
        """Detect list items that look like entries but have broken link syntax.

        Walks the markdown-it AST for list items whose inline text starts
        with '[' but contain no link node. This catches broken markdown
        like '- [name(url)' where the closing '](' is missing.
        """
        md = MarkdownIt("commonmark")
        root = SyntaxTreeNode(md.parse(self.readme_text))

        # Find category section boundaries (between Projects and Resources/Contributing)
        projects_idx = None
        end_idx = None
        for i, node in enumerate(root.children):
            if node.type == "heading" and node.tag in ("h1", "h2"):
                text = render_inline_text(node.children[0].children) if node.children else ""
                if projects_idx is None and text == "Projects":
                    projects_idx = i
                elif end_idx is None and text in ("Resources", "Contributing"):
                    end_idx = i
        if projects_idx is None:
            return

        bad = []
        cat_nodes = root.children[projects_idx + 1 : end_idx or len(root.children)]
        for node in cat_nodes:
            if node.type != "bullet_list":
                continue
            self._check_list_for_broken_links(node, bad)

        assert bad == [], "List items with broken link syntax:\n" + "\n".join(bad)

    def _check_list_for_broken_links(self, bullet_list, bad):
        for list_item in bullet_list.children:
            if list_item.type != "list_item":
                continue
            inline = _find_inline(list_item)
            if inline is None:
                continue
            # Check if inline text starts with '[' but has no link node
            has_link = any(c.type == "link" for c in inline.children)
            text = render_inline_text(inline.children)
            if not has_link and text.startswith("["):
                line = list_item.map[0] + 1 if list_item.map else "?"
                bad.append(f"  line {line}: {text}")
            # Recurse into nested lists
            for child in list_item.children:
                if child.type == "bullet_list":
                    self._check_list_for_broken_links(child, bad)



================================================
FILE: website/tests/test_scan_github_stars.py
================================================
import importlib.util
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest


@pytest.fixture
def scan(tmp_path, monkeypatch, capsys):
    script = Path(__file__).resolve().parents[2] / ".claude/skills/scan-github-stars/scripts/scan_github_stars.py"
    spec = importlib.util.spec_from_file_location("scan_github_stars", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "LEDGER", tmp_path / "starred-scan.tsv")
    monkeypatch.setattr(module, "REGISTER", tmp_path / "audit-logs.md")
    monkeypatch.setattr(module, "listed_repos", lambda: {"example/listed"})
    module.LEDGER.write_text("repo\tdate\treason\n")
    module.REGISTER.write_text("## Rejected Additions\n\n## Last Audited\n")
    now = datetime.now(UTC)
    star = {
        "full_name": "Example/Project",
        "owner": {"login": "Example"},
        "archived": False,
        "pushed_at": now.isoformat(),
        "created_at": (now - timedelta(days=100)).isoformat(),
        "language": "Python",
        "stargazers_count": 100,
        "topics": [],
        "description": "A candidate",
    }

    def run(*args, stars=None):
        monkeypatch.setattr(module.sys, "argv", [str(script), *args])
        monkeypatch.setattr(module, "gh", lambda *args: "maintainer" if args[1] == "user" else "\n".join(json.dumps(s) for s in (stars or [star])))
        module.main()
        return capsys.readouterr()

    return module, star, run


@pytest.mark.parametrize("rejected", [False, True])
def test_full_review_can_park_a_previous_verdict(scan, rejected):
    module, _, run = scan
    history = "repo\tdate\treason\nExample/Project\t2026-10-16\tno matching use case\n"
    module.LEDGER.write_text(history)
    if rejected:
        module.REGISTER.write_text("## Rejected Additions\n- example/project -- 2026-10-16: no matching use case\n")

    assert "Example/Project" not in run().out
    review = run("--full").out
    assert "Example/Project" in review
    assert ("rejected" if rejected else "screened out") in review

    module.LEDGER.write_text(history + "example/project\t2026-10-16\tparked\n")
    if rejected:
        module.REGISTER.write_text("## Rejected Additions\n")

    assert "Example/Project" in run().out
    assert module.LEDGER.read_text().startswith(history)


@pytest.mark.parametrize("decision", ["screen", "reject"])
def test_later_decision_on_same_day_excludes_parked_repo(scan, decision):
    module, _, run = scan
    history = "repo\tdate\treason\nexample/project\t2026-10-16\tparked\n"
    module.LEDGER.write_text(history)
    assert "Example/Project" in run().out

    if decision == "screen":
        module.LEDGER.write_text(history + "EXAMPLE/PROJECT\t2026-10-16\tstill no use case\n")
    else:
        module.REGISTER.write_text("## Rejected Additions\n- EXAMPLE/PROJECT -- 2026-10-16: still no use case\n")

    assert "Example/Project" not in run().out
    assert "still no use case" in run("--full").out


def test_parking_does_not_override_exact_registered_rejection(scan):
    module, _, run = scan
    module.LEDGER.write_text("repo\tdate\treason\nexample/project\t2026-10-16\tparked\n")
    module.REGISTER.write_text("## Rejected Additions\n- Example/Project -- 2026-10-16: maintainer rejection\n")

    assert "Example/Project" not in run().out
    assert "maintainer rejection" in run("--full").out


def test_parking_reopens_one_repo_from_rejected_organization(scan):
    module, star, run = scan
    module.REGISTER.write_text("## Rejected Additions\n- EXAMPLE/* -- 2026-10-16: maintainer rejection\n")
    peer = star | {"full_name": "Example/Other"}
    assert "Example/Project" not in run().out

    module.LEDGER.write_text("repo\tdate\treason\nexample/project\t2026-10-16\tparked\n")
    result = run(stars=[star, peer]).out
    assert "Example/Project" in result
    assert "Example/Other" not in result

    module.REGISTER.write_text(module.REGISTER.read_text() + "- example/project -- 2026-10-16: rejected again\n")
    assert "Example/Project" not in run().out
    assert "rejected again" in run("--full").out


def test_parking_keeps_other_exclusions(scan):
    module, star, run = scan
    now = datetime.now(UTC)
    changes = [
        {"full_name": "example/listed"},
        {"owner": {"login": "maintainer"}},
        {"archived": True},
        {"pushed_at": (now - timedelta(days=400)).isoformat()},
        {"created_at": now.isoformat()},
    ]
    for change in changes:
        candidate = star | change
        module.LEDGER.write_text(f"repo\tdate\treason\n{candidate['full_name']}\t2026-10-16\tparked\n")
        assert candidate["full_name"] not in run(stars=[candidate]).out



================================================
FILE: .claude/skills/audit-the-list/SKILL.md
================================================
---
name: audit-the-list
description: Audit README.md sections against the shortlist rules — re-verify every entry's verdict with live data, promote or demote challengers, restructure oversized use cases, prune, and evaluate proposed additions. Fire when the maintainer asks to audit, sweep, prune, re-check, or maintain sections, or asks whether an entry (or a proposed one) deserves its slot.
argument-hint: [all, specific sections, or none for a recommendation]
---

# Audit the list

An Audit re-runs the admission test over live sections of README.md: every entry re-verified against current data, tiers reassessed, structure reconsidered, then the maintainer adjudicates and the result is committed. The rules live in CONTRIBUTING.md (Admission, Evidence, Entry Ordering) — this skill is the process that applies them, not a second copy of them. Entry changes land only on the maintainer's explicit go.

## 1. Scope

Resolve the scope from the arguments. Named sections mean exactly those, whether or not they were audited before (a re-run is how a past verdict gets rechecked). `all` is ambiguous — `AskUserQuestion` whether it means every section or only never-audited ones. Batch the work one Thematic Group per sitting. Done when the section list is settled.

With no arguments, or to see which sections were never audited, run `uv run python .claude/skills/audit-the-list/scripts/audit_priority.py`. It dates each section's last audit from `audit:`/`prune: sweep` and `style: audit` commit subjects plus the Last Audited lines in `docs/audit-logs.md`, then ranks sections: entries added or removed since that audit first, most changes first, then unchanged sections by oldest audit, never-audited first. Print its ranking, then AskUserQuestion with the top four sections as options, the first marked Recommended, each description carrying its changed entries or its last-audit date. A renamed section loses its audit history and ranks as never audited; the script lists the orphaned subjects, so say so when that happens.

## 2. Evidence

Fetch live evidence for every entry in scope before judging anything (AGENTS.md verification rule):

- **Downloads/month**: `cd website && uv run python fetch_pypi_downloads_via_clickpy.py` — free keyless ClickPy sweep of the full README, sole writer of `data/pypi_downloads.tsv` (rewritten from scratch each run; header row, every row stamped with its `fetched_at` date). A cache whose `fetched_at` is within the last 7 days is current enough for verdicts — skip the sweep; older than that, re-run it (costs ~1s). Cross-checks print to stdout, take explicit names, and never touch the cache: `fetch_pypi_downloads_via_bigquery.py <name> ...` (canonical source, maintainer's own GCP account, `--dry-run` first — the docstring carries the cost constraints; full-README sweeps exceed the free tier, keep name lists small), `fetch_pypi_downloads_via_pepy.py <name> ...` (needs `PEPY_TECH_API_KEY` in repo-root `.env`, throttled to 5 requests/minute), or `https://pypistats.org/api/packages/{name}/recent` paced 8s or slower. pypistats excludes mirror/CI traffic; ClickPy, BigQuery, and pepy include it — never mix sources within one comparison.
- **Repo state**: archived flag, last push, created date, stars, description — `gh api repos/{owner}/{repo}`, GitLab API for GitLab-hosted projects.
- **PyPI metadata** (`https://pypi.org/pypi/{name}/json`) wherever a name might not be the canonical package — ownership collisions and wrong display names surface here. Wrong-package cache rows are common: the sweep looks up README display names, so when the display name differs from the canonical package, the row silently measures an unrelated squatter or a dead predecessor. When a famous entry shows a count that looks off (too small, or absurdly round), verify identity before citing it, and fetch the canonical package's count via pepy.
- **Renaming an entry can silently expose it to the sweep, and no automatic check catches that.** The sweep only queries names matching `PYPI_NAME_RE`, so a display name carrying a space or other non-PyPI shape is skipped outright. Rename it into a PyPI-shaped one and it starts being queried: `uv audit` became `uv-audit`, and PyPI `uv-audit` is an unrelated third-party tool by rocshers, not Astral's subcommand. After any rename, fetch `https://pypi.org/pypi/{new-name}/json` and confirm the package is the project the entry links to; when it is not, add a null entry to `website/data/pypi_name_overrides.json` with the reason. Only one case is guarded automatically: `test_bundled_entries_are_never_queried_on_pypi` requires a null override for every `(part of X)` entry. Two broader checks were measured against the full list and rejected — do not re-propose either. Requiring a package's PyPI metadata to link back to the entry's GitHub repo misses this case completely, since `uv-audit` declares no repo URL at all, as do 26 legitimate entries including numba, selenium and pyglet; it also flags 10 benign org moves and binding splits (gensim, msgspec, pendulum, instructor, duckdb). Flagging entries whose display name differs from their repo name returns 46 hits, every one legitimate, and `uv-build` sits among them with the shape identical to `uv-audit` despite being a real Astral package.

Done when every entry in scope has downloads (or a stated no-signal reason), repo state, and a confirmed PyPI name.

## 3. Verdicts

Draft a verdict and reason for every entry, restructure before cap: decide Splits, mints, and re-homes first — cutting before restructuring destroys entries — then apply the cap tier by tier, including promotions and demotions between obvious choice and challenger. Ground every reason in the fetched evidence; label anything unverifiable as a judgment call. Where fresh evidence contradicts the standing verdict, say so in the reason instead of silently keeping the seed. A proposed addition under `docs/audit-logs.md` "Rejected Additions" seeds as reject from that line.

## 4. Review and go

Run the `preview-verdicts` skill: it generates the interactive review page and defines how the maintainer's feedback JSON comes back and gets processed. Their verdicts are final. Before touching README.md, surface what the feedback implies but does not decide — cap overflows, homeless entries after a Split, tier for a tierless flip — as named assumptions or questions, then get an explicit go.

## 5. Execute

One commit per section: body lists each removal with its reason and downloads figure, naming the figure's source and fetch date so a later audit can tell whether a trend compares like with like (ClickPy counts mirror traffic, pypistats does not); restructures, tier moves, and reorders ride the same commit. A restructure that renames or dissolves a category or subcategory adds `"old path": "new path"` to `website/data/redirects.json` in that commit, so the old URL keeps its search ranking; the build fails when a redirect target no longer exists, so a later rename also updates the entries pointing at the renamed path. Format-only outcomes (no removals) are a single style commit whose subject starts `style: audit <Section>`. A section whose audit changes nothing gets a line under Last Audited in `docs/audit-logs.md` instead (`- <Section> -- <yyyy-mm-dd>, no changes.`, replacing its earlier line), committed, since the ranking script reads an audit only from a commit or that line. `make test` before every commit. After the last add or rename, re-run the ClickPy sweep, since new names have no cache row and the build would count them without downloads, then `make build`. Generic commit helpers tend to split a section audit into structural and per-subcategory commits — if that happens, squash back to one commit per section. Done when the tree is clean, tests passed before each commit, and the build count reconciles with the adjudicated changes.

## 6. Record

A conclusion that outlives the sitting goes into the repo before the audit ends: admission or evidence rules into CONTRIBUTING.md, repo process and environment facts into AGENTS.md. Done when nothing the next audit needs is stranded in conversation.



================================================
FILE: .claude/skills/audit-the-list/scripts/audit_priority.py
================================================
"""Rank README.md sections for the next audit.

A section's last audit is the newest of: a commit whose subject starts with
`audit: sweep`, `prune: sweep`, or `style: audit` and names the section or its
Thematic Group, and its line under docs/audit-logs.md "Last Audited". A commit
on a merged branch dates from that merge. Sections whose entries changed since
then come first, most changes first; the rest
follow by oldest audit, never-audited first.
"""

import re
import subprocess
import sys
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "website"))

from readme_parser import parse_readme

# The shortlist reform; audits start after it, and never-audited sections diff against it.
REFORM = "553bf88"
AUDIT_SUBJECT_RE = re.compile(r"^(?:(?:audit|prune): sweep|style: audit) (.+?)(?: —|,| to the shortlist cap|$)")
REGISTER_LINE_RE = re.compile(r"^- (.+?) -- (\d{4}-\d{2}-\d{2})")


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True).stdout


@cache
def entries_at(rev: str) -> dict[str, dict[str, set[str]]]:
    """Section -> {display name: {normalized name, normalized URL}}.

    An entry matches across revisions on either key, so a rename that keeps its link, or a link fix that keeps its name, is no change.
    """
    sections = {}
    for group in parse_readme(git("show", f"{rev}:README.md")):
        for category in group["categories"]:
            links = [*category["entries"], *(sub for entry in category["entries"] for sub in entry["also_see"])]
            sections[category["name"]] = {link["name"]: {re.sub(r"[-_.]+", "-", link["name"]).lower(), link["url"].rstrip("/").lower()} for link in links}
    return sections


def missing(entries: dict[str, set[str]], other: dict[str, set[str]]) -> list[str]:
    """Display names in entries that match no entry in other."""
    keys = set().union(*other.values())
    return [name for name, own in entries.items() if not own & keys]


def resolve(text: str, groups: dict[str, list[str]]) -> list[str]:
    """Sections named in text, longest name first so "Database Drivers" never counts as "Database"."""
    found = []
    for name in sorted(groups, key=len, reverse=True):
        if re.search(rf"(?<!\w){re.escape(name)}(?!\w)", text):
            found.extend(groups[name])
            text = text.replace(name, "")
    return found


def main() -> None:
    current = parse_readme(git("show", "HEAD:README.md"))
    group_of = {c["name"]: g["name"] for g in current for c in g["categories"]}
    # Section names map to themselves, Thematic Group names to all their sections.
    names = {s: [s] for s in group_of} | {g["name"]: [c["name"] for c in g["categories"]] for g in current}

    last: dict[str, tuple[int, str, str]] = {}  # section -> (timestamp, date, rev)

    def stamp(section: str, timestamp: int, date: str, rev: str) -> None:
        if section not in last or timestamp > last[section][0]:
            last[section] = (timestamp, date, rev)

    # Branch commit -> the merge that landed it, so an audit's follow-up `feat: add` commits count as audited.
    landed = {commit: merge for merge in git("rev-list", "--first-parent", "--merges", f"{REFORM}..HEAD").split() for commit in git("rev-list", f"{merge}^1..{merge}").split()}

    unmatched = []
    for line in git("log", "--format=%H%x09%ct%x09%cs%x09%s", f"{REFORM}..HEAD").splitlines():
        rev, timestamp, date, subject = line.split("\t", 3)
        rev = landed.get(rev, rev)
        if match := AUDIT_SUBJECT_RE.match(subject):
            sections = resolve(match.group(1), names)
            for section in sections:
                stamp(section, int(timestamp), date, rev)
            if not sections:
                unmatched.append(subject)

    register = (ROOT / "docs" / "audit-logs.md").read_text().splitlines()
    start = register.index("## Last Audited")
    for lineno, line in enumerate(register[start:], start + 1):
        if match := REGISTER_LINE_RE.match(line):
            blame = git("blame", "--porcelain", "-L", f"{lineno},{lineno}", "--", "docs/audit-logs.md").splitlines()
            rev = blame[0].split()[0]
            if set(rev) == {"0"}:  # uncommitted line
                rev = "HEAD"
            timestamp = int(next(b.split()[1] for b in blame if b.startswith("committer-time ")))
            for section in resolve(match.group(1), names):
                stamp(section, timestamp, match.group(2), rev)

    head = entries_at("HEAD")
    changed, unchanged = [], []
    for section in group_of:
        _, date, rev = last.get(section, (0, "never", REFORM))
        before = entries_at(rev).get(section, {})
        added = missing(head[section], before)
        removed = missing(before, head[section])
        row = (section, date, rev[:7] if section in last else "", added, removed)
        (changed if added or removed else unchanged).append(row)

    # "never" sorts after digits, so map it to "" to put never-audited first.
    changed.sort(key=lambda r: (-(len(r[3]) + len(r[4])), "" if r[1] == "never" else r[1]))
    unchanged.sort(key=lambda r: "" if r[1] == "never" else r[1])

    print("Entries added or removed since last audit:")
    for section, date, rev, added, removed in changed:
        diff = " ".join([*(f"+{n}" for n in sorted(added)), *(f"-{n}" for n in sorted(removed))])
        print(f"  {section} [{group_of[section]}]  last {date} {rev}  {diff}")
    print("\nNo entry changes, oldest audit first:")
    for section, date, rev, _, _ in unchanged:
        print(f"  {section} [{group_of[section]}]  last {date} {rev}")
    if unmatched:
        print("\nAudit subjects naming no current section or group (renamed or dissolved since):")
        for subject in unmatched:
            print(f"  {subject}")


if __name__ == "__main__":
    main()



================================================
FILE: .claude/skills/preview-verdicts/SKILL.md
================================================
---
name: preview-verdicts
description: Generate the interactive keep/remove/add/reject verdict preview (HTML page with per-row feedback controls) whenever a prune sweep, batch entry edit, or restructure needs maintainer review before touching README.md — and process the feedback JSON the maintainer pastes back.
---

# Verdict preview

Maintainer review happens through an interactive HTML page: one row per entry with your seeded verdict and reason, verdict buttons and a reason field for the maintainer, and a **Copy feedback** button that exports only changed or commented rows as JSON. Generate the page, wait for the pasted JSON, then apply it. Entry changes land in README.md only after the review — and only on an explicit go.

## Generate the preview

1. Build the `DATA` array. A group is `[section, subcategory, rows]`; a row is `[entry, url, downloads, kind, verdict, reason]`, plus an optional seventh `source` field.
   - `source` says where a row came from when that is not obvious, such as the starred repo behind a scan candidate or an incumbent pulled in during the audit. The page shows a Source column only when a row has one.
   - `subcategory` may carry a note after ` — ` (rendered muted): use it for proposed splits, re-homes, or anything the maintainer should weigh for the whole group.
   - `downloads` is PyPI last-month as a comma-formatted string; use `—` when no signal exists (e.g. agent skill packs), `stdlib` for standard-library modules, `fetch failed` when the lookup failed. State the fetch date in the sub-header.
   - `kind` sets the buttons independently of the seeded `verdict`:
     - `listed`: `keep`, `remove` (taken out of README.md), or `park`.
     - `candidate`: `add`, `reject` (not added, logged under "Rejected Additions"), or `park`.
     - `structure`: `restructure` (take the change the reason or group note describes), `park`, or `reject` (logged under "Rejected Additions").
   - Seed `verdict` from the current adjudication or dry-run. `park` defers a decision for a later review; preserve the row's `kind` so its original choices remain available.
   - Show a replacement as two rows: the old entry `listed` / `remove`, the new entry `candidate` / `add`.
   - `reason` is plain language the maintainer reads cold — no invented shorthand. When fresh evidence contradicts the seeded verdict (a big download count on a remove or reject, a dead repo on a keep), say so in that row's reason instead of silently changing the seed.
2. Copy `template.html` (sibling of this file) and replace the placeholders: `__TITLE__` (page title), `__SUB__` (sub-header: scope, seed provenance, fetch date, and the standing instruction to flip/comment then Copy feedback), `__KEY__` (localStorage key), `__DATA__` (the array). `__KEY__` must be unique per review — slug plus date, e.g. `awesome-python-science-2026-09-01` — because saved state under a reused key bleeds a previous review's flips into rows with the same section and entry name.
3. Write the page to `local/awesome-python-<slug>-preview.html` in the repo root (git-ignored; create the directory if needed), `open` it, and tell the maintainer the path and the return path: flip or comment rows (they highlight yellow), press **Copy feedback**, paste the JSON into the chat. Done when the page is open and the return path is stated.

## Process the pasted feedback

Each JSON row is `{section, subcategory, entry, kind, my_verdict, your_verdict, reason}`, with kinds and verdicts as defined above. The maintainer's verdict is final — apply it, never re-argue it. An empty reason means the verdict stands unexplained; that is enough.

Before executing, surface anything the flips imply that the maintainer has not decided: a use case pushed past its cap, an entry left homeless by a proposed split, a request that is already satisfied (a no-op). Ask, then execute on their go. Done when every pasted row is either applied or surfaced back — none silently dropped.



================================================
FILE: .claude/skills/preview-verdicts/template.html
================================================
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  :root {
    --ink: #1c1917; --paper: #faf9f7; --muted: #78716c; --line: #e7e5e4;
    --keep: #1d4ed8; --keep-bg: #eff4ff; --add: #6d28d9; --add-bg: #f3efff; --drop: #b42318; --drop-bg: #fdf1ef;
    --changed: #fffbeb; --changed-line: #f5c518;
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--paper); color: var(--ink); font: 16px/1.5 -apple-system, "SF Pro Text", "Helvetica Neue", Arial, sans-serif; }
  .wrap { padding: 2rem 2.5rem 6rem; }
  h1 { font-size: 1.7rem; margin: 0 0 .3rem; }
  .sub { color: var(--muted); margin: 0 0 1.6rem; font-size: 1rem; }
  .sub b { color: var(--ink); }
  .sub code { background: #f0eeec; padding: .1em .35em; border-radius: 4px; font-size: .92em; }
  h2 { font-size: 1.35rem; margin: 2.2rem 0 .2rem; border-bottom: 2px solid var(--ink); padding-bottom: .3rem; }
  h3 { font-size: 1.05rem; margin: 1.3rem 0 .4rem; color: var(--ink); }
  h3 .note { font-weight: 400; color: var(--muted); font-size: .92rem; }
  table { width: 100%; border-collapse: collapse; }
  th { text-align: left; font-size: .82rem; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); padding: .35rem .6rem; border-bottom: 1px solid var(--line); }
  td { padding: .5rem .6rem; border-bottom: 1px solid var(--line); vertical-align: top; }
  tr.changed td { background: var(--changed); border-bottom-color: var(--changed-line); }
  td.name { white-space: nowrap; font-weight: 600; }
  td.name a { color: var(--ink); text-decoration: none; border-bottom: 1px solid #c8c4c0; }
  td.name a:hover { border-bottom-color: var(--ink); }
  td.source { font-size: .95rem; color: var(--muted); max-width: 14rem; }
  td.dl { white-space: nowrap; font-variant-numeric: tabular-nums; color: var(--muted); text-align: right; }
  td.mine { white-space: nowrap; }
  .badge { display: inline-block; font-size: .78rem; font-weight: 700; letter-spacing: .03em; padding: .12em .5em; border-radius: 4px; }
  .badge.keep { color: var(--keep); background: var(--keep-bg); }
  .badge.remove, .badge.reject { color: var(--drop); background: var(--drop-bg); }
  .badge.add, .badge.restructure { color: var(--add); background: var(--add-bg); }
  .badge.park { color: var(--muted); background: var(--line); }
  td.reason { color: #44403c; font-size: .95rem; max-width: 34rem; }
  td.yours { white-space: nowrap; }
  .seg { display: inline-flex; border: 1px solid var(--line); border-radius: 6px; overflow: hidden; }
  .seg button { border: 0; background: #fff; padding: .3rem .8rem; font: inherit; font-size: .88rem; cursor: pointer; color: var(--muted); }
  .seg button + button { border-left: 1px solid var(--line); }
  .seg button.on { color: #fff; font-weight: 700; }
  .seg button.on.keep { background: var(--keep); }
  .seg button.on.add, .seg button.on.restructure { background: var(--add); }
  .seg button.on.remove, .seg button.on.reject { background: var(--drop); }
  .seg button.on.park { background: var(--muted); }
  td.fb input { width: 100%; min-width: 14rem; font: inherit; font-size: .92rem; padding: .3rem .5rem; border: 1px solid var(--line); border-radius: 6px; background: #fff; }
  td.fb input:focus { outline: 2px solid var(--keep); outline-offset: 0; }
  .bar { position: fixed; bottom: 0; left: 0; right: 0; background: var(--ink); color: #fafaf9; display: flex; align-items: center; gap: 1.4rem; padding: .7rem 2.5rem; font-size: .95rem; }
  .bar .counts b { font-variant-numeric: tabular-nums; }
  .bar button { font: inherit; font-weight: 700; padding: .45rem 1.1rem; border: 0; border-radius: 6px; background: #fafaf9; color: var(--ink); cursor: pointer; }
  .bar button:hover { background: #e7e5e4; }
  .bar .hint { color: #a8a29e; }
  #out { display: none; width: 100%; height: 9rem; margin-top: 1rem; font: 13px/1.4 ui-monospace, monospace; }
</style>
</head>
<body>
<div class="wrap">
  <h1>__TITLE__</h1>
  <p class="sub">__SUB__</p>
  <div id="app"></div>
  <textarea id="out" readonly></textarea>
</div>
<div class="bar">
  <span class="counts" id="counts"></span>
  <button onclick="copyFeedback()">Copy feedback</button>
  <span class="hint" id="hint">Copies only rows you changed or commented, as JSON.</span>
</div>
<script>
const DATA = __DATA__;

const KEY = "__KEY__";
let state = {};
try { state = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) {}

const CHOICES = { listed: ["keep", "remove", "park"], candidate: ["add", "reject", "park"], structure: ["restructure", "park", "reject"] };
const cap = v => v[0].toUpperCase() + v.slice(1);

function rowId(section, name) { return section + "::" + name; }

function render() {
  const app = document.getElementById("app");
  let html = "", lastSection = "";
  const hasSource = DATA.some(g => g[2].some(r => r.length > 6));
  for (const [section, subcat, rows] of DATA) {
    if (section !== lastSection) { html += `<h2>${section}</h2>`; lastSection = section; }
    const parts = subcat.split(" — ");
    html += `<h3>${parts[0]}${parts[1] ? ` <span class="note">— ${parts[1]}</span>` : ""}</h3>`;
    html += `<table><tr><th>Entry</th>${hasSource ? "<th>Source</th>" : ""}<th style="text-align:right">Downloads/mo</th><th>My verdict</th><th>My reason</th><th>Yours</th><th>Your reason (optional)</th></tr>`;
    for (const [name, url, dl, kind, mine, reason, source] of rows) {
      const id = rowId(section, name);
      const s = state[id] || {};
      const yours = s.verdict || mine;
      const changed = yours !== mine || (s.feedback || "").trim() !== "";
      html += `<tr id="${cssId(id)}" class="${changed ? "changed" : ""}">
        <td class="name"><a href="${url}" target="_blank" rel="noopener">${name}</a></td>
        ${hasSource ? `<td class="source">${source || ""}</td>` : ""}
        <td class="dl">${dl}</td>
        <td class="mine"><span class="badge ${mine}">${mine.toUpperCase()}</span></td>
        <td class="reason">${reason}</td>
        <td class="yours"><span class="seg">
          ${CHOICES[kind].map(v => `<button class="${v} ${yours === v ? "on" : ""}" onclick="setV('${esc(id)}','${v}')">${cap(v)}</button>`).join("")}
        </span></td>
        <td class="fb"><input value="${(s.feedback || "").replace(/"/g, "&quot;")}" oninput="setF('${esc(id)}', this.value)" placeholder="why…"></td>
      </tr>`;
    }
    html += `</table>`;
  }
  app.innerHTML = html;
  updateCounts();
}

function cssId(id) { return "r-" + id.replace(/[^a-zA-Z0-9]/g, "_"); }
function esc(id) { return id.replace(/'/g, "\\'"); }

function setV(id, v) { state[id] = state[id] || {}; state[id].verdict = v; save(); render(); }
function setF(id, f) {
  state[id] = state[id] || {}; state[id].feedback = f; save();
  const [section, name] = id.split("::");
  const mine = findMine(section, name);
  const yours = state[id].verdict || mine;
  document.getElementById(cssId(id)).className = (yours !== mine || f.trim() !== "") ? "changed" : "";
  updateCounts();
}
function findMine(section, name) {
  for (const [s, , rows] of DATA) if (s === section) for (const r of rows) if (r[0] === name) return r[4];
}
function save() { localStorage.setItem(KEY, JSON.stringify(state)); }

function collect() {
  const out = [];
  for (const [section, subcat, rows] of DATA) {
    for (const [name, , , kind, mine] of rows) {
      const id = rowId(section, name);
      const s = state[id] || {};
      const yours = s.verdict || mine;
      const fb = (s.feedback || "").trim();
      if (yours !== mine || fb) out.push({ section, subcategory: subcat.split(" — ")[0], entry: name, kind, my_verdict: mine, your_verdict: yours, reason: fb });
    }
  }
  return out;
}

function updateCounts() {
  const tally = {};
  let changed = 0;
  for (const [section, , rows] of DATA) for (const [name, , , , mine] of rows) {
    const s = state[rowId(section, name)] || {};
    const yours = s.verdict || mine;
    tally[yours] = (tally[yours] || 0) + 1;
    if (yours !== mine) changed++;
  }
  const counts = Object.entries(tally).map(([v, n]) => `<b>${n}</b> ${v}`).join(" · ");
  document.getElementById("counts").innerHTML = `${counts} &nbsp;|&nbsp; <b>${changed}</b> verdicts flipped`;
}

function copyFeedback() {
  const fb = collect();
  const text = fb.length ? JSON.stringify(fb, null, 1) : `(no changes — all verdicts accepted as-is: ${document.title} — ${[...new Set(DATA.map(g => g[0]))].join(", ")})`;
  const hint = document.getElementById("hint");
  navigator.clipboard.writeText(text).then(
    () => { hint.textContent = `Copied ${fb.length ? fb.length + " row(s)" : "acceptance note"} — paste into the chat.`; },
    () => { const o = document.getElementById("out"); o.style.display = "block"; o.value = text; o.select(); hint.textContent = "Clipboard blocked — select & copy the box above."; }
  );
}

render();
</script>
</body>
</html>



================================================
FILE: .claude/skills/review-prs/SKILL.md
================================================
---
name: review-prs
description: Triage open PRs — screen from the diff, delegate the admission judgment to audit-the-list, then merge or close on GitHub. Fire when the maintainer asks to review PRs, process the PR queue, or judge whether a specific PR should be merged.
argument-hint: [PR numbers]
---

# Review PRs

A PR review turns the open queue into terminal states: merged, closed, or explicitly parked. The rules live in CONTRIBUTING.md (Quality Requirements, Admission, Review Process, Automatic Rejection) — this skill is the workflow that applies them, not a second copy. Every PR named in chat is a PR link, `[#<number>](https://github.com/vinta/awesome-python/pull/<number>)`, so the maintainer can open it from the terminal.

## 1. Fetch

Arguments name specific PRs; otherwise take the queue: `gh pr list --repo vinta/awesome-python --limit 10 --json number,title,author,url,body,files,mergeable,mergeStateStatus`. Fetch all diffs in parallel: `gh pr diff <number> --repo vinta/awesome-python`.

Sort the batch: entry additions continue; anything else (typo fixes, website changes, docs) is out of scope — report it under "needs human" and touch nothing, so it resurfaces every run until a human acts. Done when every PR is sorted and has its diff.

## 2. Screen

Apply the Automatic Rejection rules that the diff and PR metadata answer without judgment. The recently-closed-duplicate rule needs a lookup: `gh pr list --repo vinta/awesome-python --state closed --search "<project name>" --limit 10`; a project under `docs/audit-logs.md` "Rejected Additions" also counts as previously rejected unless the PR brings evidence newer than its line. A screened-out PR goes straight to step 4 as a close, with the rule it broke as its reason.

Resolve each survivor's target use case against the current README — a diff's context lines show the base the PR was written on, which may have changed since. A merge conflict rides to the Merge arm, which absorbs it. Done when every surviving PR names its target use case.

## 3. Judge

Group survivors by target use case — PRs proposing entries for the same use case compete for the same slots, so they ride one invocation. Per group, invoke the `audit-the-list` skill with arguments in this shape: "Judge proposed entries <names, each with its PR number> for the <section — subcategory> use case. Evidence and Verdicts steps only; report the verdicts back. No preview page, no README changes, no commits." The verdict for each PR is merge or close, grounded in the fetched evidence; when the use case is at cap, a merge verdict names the entry that leaves. An entry no current use case fits is a third outcome — a structure question: carry it to Act with evidence attached, and the maintainer decides there (mint the subcategory and merge, close, or leave open). Done when every survivor holds a verdict with a reason.

## 4. Act

- **Close**: draft each closing comment — it states the reason and links CONTRIBUTING.md. Per batch of up to 4 closing PRs: print each draft in chat, its PR link as a label above a fenced block holding only the comment bytes, then AskUserQuestion over that batch — arms: close with the draft as printed, close without a comment, keep open. The chat print is the review copy; an option description only points at it. Keep a checklist of which verdicts have been asked; answers often arrive as custom text, and that text is the decision — an edited comment replaces the draft. Then `gh pr close <number> --repo vinta/awesome-python --comment "<comment>"`, or a plain close.
- **Merge**: a clean PR merges with `gh pr merge <number> --repo vinta/awesome-python --merge`. A conflicted one merges locally: `git fetch origin pull/<number>/head`, `git merge FETCH_HEAD` with the standard `Merge pull request #<number> from <owner>/<headRef>` message, resolving the conflict by placing the entry correctly — GitHub still marks the PR merged and the contributor keeps credit. Either way, reconcile the section per CONTRIBUTING before pushing: remove the entry the verdict displaced, fix the new entry's display name and Entry Ordering position, `make test`, commit. An add-only diff that displaces is the normal case — the removal is this step's job, not the contributor's.
Done when every verdict has been adjudicated by the maintainer and its action executed, with every posted comment byte-identical to a printed draft or to the custom text the maintainer supplied. A kept-open PR resurfaces next run — that is its point.

## 5. Report

Summary table: PR link, verdict, action taken, plus the needs-human list. Done when every fetched PR ends in exactly one state — merged with its section reconciled, closed, or left open (kept open, needs-human, or structure question pending).



================================================
FILE: .claude/skills/scan-github-stars/SKILL.md
================================================
---
name: scan-github-stars
description: Scan the maintainer's GitHub stars for README.md addition candidates; incremental by default, `full` rejudges stars judged before.
argument-hint: [incremental | full]
---

# Scan GitHub stars

A star scan turns the maintainer's GitHub stars into proposed additions. Every star the scan sees ends in one place: listed in README.md, screened out in `local/starred-scan.tsv`, rejected under `docs/audit-logs.md` "Rejected Additions", or parked for another review. Judgment belongs to `audit-the-list` and the rules to CONTRIBUTING.md; this skill only sources candidates and records outcomes.

## 1. Scan

Run `uv run python .claude/skills/scan-github-stars/scripts/scan_github_stars.py`, adding `--full` when the argument is `full`. With no ledger yet, a plain run already covers every star. Print the drop counts from stderr. Done when the candidate TSV is in hand.

## 2. Screen

Judge each candidate from its name, description, topics, and language against CONTRIBUTING Quality Requirement 1 (Serves Python Developers), and name the current use case it would compete in. The screen is loose: drop only what plainly fails, and pass anything uncertain on, since `audit-the-list` is the real judge. In a full scan, read the `prior` column as context and overturn a rejection only on new evidence.

Append each screen-out to `local/starred-scan.tsv` as it is decided, one `repo<TAB>yyyy-mm-dd<TAB>reason` row (create the file with header `repo	date	reason`), so an interrupted run keeps its work. The file is append-only; the script reads the last row per repo. A survivor no current use case fits is a structure question: carry it to review with its evidence. Done when every candidate is a ledger row, holds a target use case, or is a structure question.

## 3. Judge

Group survivors by target use case. Per group, invoke `audit-the-list` with: "Judge proposed entries <names, each with its GitHub repo> for the <section — subcategory> use case. Evidence and Verdicts steps only; report the verdicts back. No preview page, no README changes, no commits." A reject whose reason names an unlisted project as the better pick turns that project into a candidate too: judge it in the same group and mark its source as found in the audit, not starred. Done when every survivor holds an add or reject verdict with a reason, and each add at cap names the entry it displaces.

## 4. Review

Run `preview-verdicts` over all groups: survivors with kind `candidate` and verdict `add` or `reject`, displaced entries with kind `listed` and verdict `remove`, and structure questions with kind `structure` and verdict `park` or `restructure`. Quote any `prior` verdict in the reason. Seed `park` on any row whose verdict rests on a judgment call, except an add where only the tier is in doubt; preserve its kind. Done when the maintainer's feedback is processed and they gave the go.

## 5. Record

- **Added**: follow `audit-the-list` step 5 for the README change, one commit per entry. When the entry links a different repo than the star (a Python binding or client of a starred engine), also append a ledger row `already listed as <entry> (<owner/repo>)` for the star, since the script only recognizes a star whose own repo is linked.
- **Rejected**: a candidate with verdict `reject` gets one line under "Rejected Additions": `- owner/repo -- yyyy-mm-dd, <downloads>/month (<source>): <reason>.`, replacing its earlier line. This exact rejection takes precedence over a parked ledger row.
- **Parked**: leave listed entries in README.md. An unlisted repo with no prior decision needs no record. To reopen one screened out or rejected before, remove its exact "Rejected Additions" line and append `owner/repo<TAB>yyyy-mm-dd<TAB>parked` to the ledger. Its earlier screen-out rows stay as history. The marker also exempts this repo from an `owner/*` rejection; leave that organization line in place for its other repos. A later screen-out or exact rejection excludes the repo again. A new organization-wide rejection must explicitly resolve any parked exceptions it is intended to cover.

Done when every candidate from step 1 is listed in README.md, a ledger row, a Rejected Additions line, or parked by the maintainer.



================================================
FILE: .claude/skills/scan-github-stars/scripts/scan_github_stars.py
================================================
"""List the maintainer's GitHub stars that could be README.md candidates.

Drops stars that fail a check needing no judgment: already listed, own repo,
archived, no push in 12 months, or created under a month ago. These drops are
recomputed every run, so a repo that becomes active again resurfaces. An
incremental run also drops stars already judged: model screen-outs in
local/starred-scan.tsv and maintainer rejections under docs/audit-logs.md
"Rejected Additions". `--full` keeps them and shows the earlier verdict in the
`prior` column. Prints survivors as TSV on stdout, drop counts on stderr.
"""

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import TypedDict

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "website"))

from readme_parser import parse_readme

LEDGER = ROOT / "local" / "starred-scan.tsv"
REGISTER = ROOT / "docs" / "audit-logs.md"
GITHUB_REPO_RE = re.compile(r"^https://github\.com/([^/#?]+/[^/#?]+)")
REJECTED_LINE_RE = re.compile(r"^- (\S+) -- (.+)$")


class Owner(TypedDict):
    login: str


class Star(TypedDict):
    full_name: str
    owner: Owner
    archived: bool
    pushed_at: str
    created_at: str
    language: str | None
    stargazers_count: int
    topics: list[str]
    description: str | None


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=True).stdout


def listed_repos() -> set[str]:
    repos = set()
    for group in parse_readme((ROOT / "README.md").read_text()):
        for category in group["categories"]:
            for link in [*category["entries"], *(sub for entry in category["entries"] for sub in entry["also_see"])]:
                if match := GITHUB_REPO_RE.match(link["url"]):
                    repos.add(match.group(1).removesuffix(".git").lower())
    return repos


def prior_verdicts() -> dict[str, str | None]:
    """The last ledger row wins; `parked` reopens a repo. An exact registered rejection still wins."""
    prior: dict[str, str | None] = {}
    if LEDGER.exists():
        for line in LEDGER.read_text().splitlines()[1:]:
            repo, date, reason = line.split("\t", 2)
            if reason == "parked":
                prior[repo.lower()] = None
            else:
                prior[repo.lower()] = f"screened out {date}: {reason}"
    register = REGISTER.read_text().splitlines()
    start = register.index("## Rejected Additions")
    for line in register[start + 1 :]:
        if line.startswith("## "):
            break
        if match := REJECTED_LINE_RE.match(line):
            prior[match.group(1).lower()] = f"rejected {match.group(2)}"
    return prior


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--full", action="store_true", help="rejudge stars already screened out or rejected")
    args = parser.parse_args()

    now = datetime.now(UTC)
    login = gh("api", "user", "--jq", ".login").strip().lower()
    listed = listed_repos()
    prior = prior_verdicts()

    stars: list[Star] = [json.loads(line) for line in gh("api", "--paginate", "user/starred?per_page=100", "--jq", ".[]").splitlines()]
    dropped = Counter()
    print("repo\tlanguage\tstars\tpushed\ttopics\tdescription\tprior")
    for star in stars:
        repo = star["full_name"].lower()
        verdict = prior[repo] if repo in prior else prior.get(f"{star['owner']['login'].lower()}/*")
        if repo in listed:
            dropped["already listed"] += 1
        elif star["owner"]["login"].lower() == login:
            dropped["own repo"] += 1
        elif star["archived"]:
            dropped["archived"] += 1
        elif datetime.fromisoformat(star["pushed_at"]) < now - timedelta(days=365):
            dropped["no push in 12 months"] += 1
        elif datetime.fromisoformat(star["created_at"]) > now - timedelta(days=30):
            dropped["created under a month ago"] += 1
        elif verdict and not args.full:
            dropped["judged before"] += 1
        else:
            description = " ".join((star["description"] or "").split())
            print("\t".join([star["full_name"], star["language"] or "-", str(star["stargazers_count"]), star["pushed_at"][:10], ",".join(star["topics"]), description, verdict or ""]))

    print(f"{len(stars)} stars; {len(stars) - dropped.total()} candidates", file=sys.stderr)
    for reason, count in dropped.most_common():
        print(f"  dropped {count}: {reason}", file=sys.stderr)


if __name__ == "__main__":
    main()



================================================
FILE: .github/FUNDING.yml
================================================
open_collective: awesome-python
custom: https://awesome-python.com/sponsorship/



================================================
FILE: .github/PULL_REQUEST_TEMPLATE.md
================================================
## Project

[project-name](url)

## Checklist

- [ ] I read [CONTRIBUTING.md](https://github.com/vinta/awesome-python/blob/master/CONTRIBUTING.md) - awesome-python is a shortlist, not a catalog
- [ ] One project per PR
- [ ] PR title format: `Add project-name`
- [ ] Entry format: `- [pypi-name](https://github.com/owner/repo) - Description ending with period.`
- [ ] Display name is the PyPI package name
- [ ] Placed in an existing use case (new sections and subcategories are maintainer-only)
- [ ] Meets all Quality Requirements: active, stable, documented, at least 1 month old

## Which Tier

Pick one:

- [ ] **Obvious choice** - a tool an experienced Python developer would name when asked "what do I use for this?"
- [ ] **Challenger** - not yet the obvious choice, but a credible successor to one. Give adoption-trajectory evidence, not popularity alone.

Explain:

## Displacement

If the use case is at its cap, name the entry your project replaces and argue that yours does that entry's job better. One in, one out.



================================================
FILE: .github/workflows/ci.yml
================================================
name: CI

on:
  push:
    branches: [master]
  pull_request:

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.head_ref || github.run_id }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - name: Install uv
        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
        with:
          enable-cache: true

      - name: Install dependencies
        run: uv sync --group build --locked

      - name: Run tests
        run: make test

      - name: Build website
        run: make build



================================================
FILE: .github/workflows/deploy-website.yml
================================================
name: Deploy Website

on:
  push:
    branches: [master]
  schedule:
    - cron: "0 0 * * *"

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  deploy:
    if: github.repository == 'vinta/awesome-python'
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: https://awesome-python.com/
    steps:
      - uses: actions/checkout@v7
        with:
          # build.py reads each page's last change from git history for the sitemap's lastmod
          fetch-depth: 0

      - name: Install uv
        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
        with:
          enable-cache: true

      - name: Install dependencies
        run: uv sync --group build --locked

      - name: Run tests
        if: github.event_name == 'schedule'
        run: make test

      - name: Get date
        id: date
        run: echo "today=$(date -u +%Y-%m-%d)" >> "$GITHUB_OUTPUT"

      - name: Restore star data cache
        id: cache-stars
        uses: actions/cache/restore@v6
        with:
          path: website/data/github_stars.json
          key: github-stars-${{ steps.date.outputs.today }}
          restore-keys: github-stars-

      - name: Fetch GitHub stars
        id: fetch-stars
        continue-on-error: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: make fetch_github_stars

      - name: Save star data cache
        if: steps.fetch-stars.outcome == 'success'
        uses: actions/cache/save@v6
        with:
          path: website/data/github_stars.json
          key: github-stars-${{ steps.date.outputs.today }}

      - name: Verify star data exists
        run: |
          if [ ! -f website/data/github_stars.json ]; then
            echo "::error::github_stars.json not found. No cache and fetch failed or was skipped."
            exit 1
          fi
          python -m json.tool website/data/github_stars.json > /dev/null

      - name: Restore PyPI download data cache
        uses: actions/cache/restore@v6
        with:
          path: website/data/pypi_downloads.tsv
          key: pypi-downloads-${{ steps.date.outputs.today }}
          restore-keys: pypi-downloads-

      - name: Fetch PyPI downloads
        id: fetch-downloads
        continue-on-error: true
        run: make fetch_pypi_downloads

      - name: Save PyPI download data cache
        if: steps.fetch-downloads.outcome == 'success'
        uses: actions/cache/save@v6
        with:
          path: website/data/pypi_downloads.tsv
          key: pypi-downloads-${{ steps.date.outputs.today }}

      - name: Build website
        run: make build

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v5
        with:
          path: website/output/

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v5

