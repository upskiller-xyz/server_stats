<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/upskiller-xyz/server_template">
    <img src="https://github.com/upskiller-xyz/DaylightFactor/blob/main/docs/images/logo_upskiller.png" alt="Logo" height="100" >
  </a>

  <h3 align="center">Server Stats</h3>

  <p align="center">
    REST API for calculating statistical metrics on matrices with binary masks
    <br />
    <a href="https://github.com/upskiller-xyz/server_stats">View Demo</a>
    ·
    <a href="https://github.com/upskiller-xyz/server_stats/issues">Report Bug</a>
    ·
    <a href="https://github.com/upskiller-xyz/server_stats/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a>
        <li><a href="#api-endpoints">API Endpoints</a></li>
        <li><a href="#deployment">Deployment</a>
          <li><a href="#locally">Local deployment</a></li>
        </li>
    </li>
    <li><a href="#design">Design</a>
      <li><a href="#architecture">Architecture</a></li>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contribution">Contribution</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#attribution">Attribution</a></li>
    <li><a href="#trademark-notice">Trademark notice</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Server Stats is a Flask-based REST API for calculating statistical metrics on numerical matrices with binary masks. Built with strict OOP principles, it provides a clean, scalable architecture for metric calculation services.



<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* [Python 3.13+](https://www.python.org/downloads/)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/upskiller-xyz/server_stats.git
   cd server_stats
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the server:
   ```sh
   python main.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

### 🎯 Interactive Demo

**Start here!** For hands-on examples, see the **[Playground Notebook](examples/demo.ipynb)**:

```bash
jupyter notebook examples/demo.ipynb
```

### 🔧 API Endpoints

See full documentation at **[docs/api.md](docs/api.md)**

#### POST /run
Calculate metrics on matrix with binary mask:

```python
import requests

response = requests.post("http://localhost:5000/run", json={
    "matrix": [[1.5, 2.3, 3.7], [4.2, 5.8, 6.1]],
    "mask": [[1, 1, 0], [1, 0, 1]]
})

print(response.json())
# {"metrics": {"mean": 3.45, "median": 3.7, ...}}
```

#### GET /health
Health check endpoint:

```python
response = requests.get("http://localhost:5000/health")
# {"status": "healthy"}
```

### Deployment

#### Environment Configuration
Create a `.env` file with required configurations:
```sh
MODEL=df_default_2.0.0
PORT=8000
GCP_REGION=us-central1
SERVER_NAME=model-server
REPO_NAME=server_template
IMAGE_NAME=model-server

SCW_REGISTRY_NAMESPACE=nsp
SCW_PROJECT_ID=project-id
SCW_SERVER=serve-container
SCW_IMAGE=server_template
```

#### Docker Deployment
Build and run using Docker:
```sh
docker build -t model-server .
docker run -p 8000:8000 model-server
```

#### Cloud Deployment
Deploy to Google Cloud Platform:
```sh
gcloud auth login
bash build.sh
```

or Scaleway:
```sh
bash build_scw.sh
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Locally

Set up the Model Server locally for development and testing:

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd server_template
   ```

2. **Install Dependencies with Poetry**
   ```bash
   poetry install
   ```

3. **Activate Virtual Environment**
   ```bash
   poetry shell
   ```

4. **Set Environment Variables (Optional)**
   ```bash
   export MODEL=df_default_2.0.0
   export PORT=8000
   ```

5. **Run the Server**
   ```bash
   python main.py
   ```
   The server will start on `http://localhost:8000` by default.

6. **Run Tests**
   ```bash
   poetry run pytest
   ```

7. **Code Quality Checks**
   ```bash
   poetry run ruff check .
   poetry run mypy .
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- DESIGN -->
## Design

### Architecture

The Model Server follows object-oriented design principles with clean separation of concerns:

```
ModelServerApplication
├── DownloadStrategy (handles model downloads)
└── StructuredLogger (logging system)
```

**Key Components:**
- **Dependency Injection**: All services are injected through constructors
- **Factory Patterns**: Services are created using factory classes
- **Strategy Pattern**: Different loading and processing strategies
  - `StandardMap` utility for adapter pattern with default values
- **Enumerator Pattern**: Enhanced enums with `ExtendedEnumMixin`
  - Methods: `by_value()`, `from_name()`, `get_members()`, `get_values()`
- **Single Responsibility**: Each class has one clear purpose
- **Abstract Base Classes**: Define contracts for implementations

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/upskiller-xyz/server_template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTION -->
## Contribution

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

**Development Guidelines:**

* Follow Object-Oriented Programming principles and design patterns
* Use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
* Follow [semantic versioning](https://semver.org/)
* Add type hints and documentation
* Write tests for new functionality
* Run `poetry run ruff check` and `poetry run mypy` before committing

See [CLAUDE.md](CLAUDE.md) for detailed development instructions.

### Top contributors:

<a href="https://github.com/upskiller-xyz/server_template/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=upskiller-xyz/server_template" alt="Top Contributors" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

See [License](./docs/LICENSE) for more details - or [read a summary](https://choosealicense.com/licenses/gpl-3.0/).

In short:

Strong copyleft. You **can** use, distribute and modify this code in both academic and commercial contexts. At the same time you **have to** keep the code open-source under the same license (`GPL-3.0`) and give the appropriate [attribution](#attribution) to the authors.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Attribution

📖 **Academic/Industry Use**: Please cite this work as described in [CITATION.cff](docs/citation/CITATION.cff), [CITE.txt](docs/citation/CITE.txt) or [ATTRIBUTION.md](docs/citation/ATTRIBUTION.md). Alternatively you can download the BibTeX file [here](docs/citation/model-server.bib) by adding it to `.tex` files by

```tex
\bibliography{model-server}
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Trademark Notice

- **"Upskiller"** is an informal collaborative name used by contributors affiliated with BIMTech Innovations AB.
- BIMTech Innovations AB owns all legal rights to the **Model Server** project.
- The GPL-3.0 license applies to code, not branding. Commercial use of the names requires permission.

Contact: [Upskiller](mailto:info@upskiller.xyz)

## Contact

Stanislava Fedorova - [e-mail](mailto:stasya.fedorova@gmail.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [README template](https://github.com/othneildrew/Best-README-Template)
* [PyTorch](https://pytorch.org/) - Deep learning framework
* [Flask](https://flask.palletsprojects.com/) - Web framework

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/upskiller-xyz/server_template.svg?style=for-the-badge
[contributors-url]: https://github.com/upskiller-xyz/server_template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/upskiller-xyz/server_template.svg?style=for-the-badge
[forks-url]: https://github.com/upskiller-xyz/server_template/network/members
[stars-shield]: https://img.shields.io/github/stars/upskiller-xyz/server_template.svg?style=for-the-badge
[stars-url]: https://github.com/upskiller-xyz/server_template/stargazers
[issues-shield]: https://img.shields.io/github/issues/upskiller-xyz/server_template.svg?style=for-the-badge
[issues-url]: https://github.com/upskiller-xyz/server_template/issues
[license-shield]: https://img.shields.io/github/license/upskiller-xyz/server_template.svg?style=for-the-badge
[license-url]: https://github.com/upskiller-xyz/server_template/blob/master/docs/LICENSE.txt