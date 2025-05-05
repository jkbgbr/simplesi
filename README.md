<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
-->


<!-- PROJECT LOGO -->
<!--
<br />
<div align="center">
  <a href="https://github.com/jkbgbr/simplesi">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">simplesi</h3>

  <p align="center">
    project_description
    <br />
    <a href="https://github.com/jkbgbr/simplesi"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/jkbgbr/simplesi">View Demo</a>
    &middot;
    <a href="https://github.com/jkbgbr/simplesi/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/jkbgbr/simplesi/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>
-->

[//]: # ()
[//]: # (<!-- TABLE OF CONTENTS -->)

[//]: # (<details>)

[//]: # (  <summary>Table of Contents</summary>)

[//]: # (  <ol>)

[//]: # (    <li>)

[//]: # (      <a href="#about-the-project">About The Project</a>)

[//]: # (      <ul>)

[//]: # (        <li><a href="#built-with">Built With</a></li>)

[//]: # (      </ul>)

[//]: # (    </li>)

[//]: # (    <li>)

[//]: # (      <a href="#getting-started">Getting Started</a>)

[//]: # (      <ul>)

[//]: # (        <li><a href="#prerequisites">Prerequisites</a></li>)

[//]: # (        <li><a href="#installation">Installation</a></li>)

[//]: # (      </ul>)

[//]: # (    </li>)

[//]: # (    <li><a href="#usage">Usage</a></li>)

[//]: # (    <li><a href="#roadmap">Roadmap</a></li>)

[//]: # (    <li><a href="#contributing">Contributing</a></li>)

[//]: # (    <li><a href="#license">License</a></li>)

[//]: # (    <li><a href="#contact">Contact</a></li>)

[//]: # (    <li><a href="#acknowledgments">Acknowledgments</a></li>)

[//]: # (  </ol>)

[//]: # (</details>)



<!-- ABOUT THE PROJECT -->
## About The Project

Simplesi is a package enabling units-aware engineering calculations. It is based on and heavily influenced by [forallpeople](https://github.com/connorferster/forallpeople), but differs from it considerably.
It schratches somewhat the itch that most such packages are quite slow. Also, this module was made with apps in head rather than interactive use (e.g. jupyter).

Compared to forallpeople:
- faster
- the concept of environments is adapted with changes.
  - SI and non-SI units are in separated environments; environment definitions are otherwise similar to forallpeople
  - loading multiple environments is allowed, hence mixing e.g. US customary and SI units is possible
- more robust operations, e.g. between scalar and Physical - no more ambiguous additions
- modified, probably more intuitive behavior of printing
- user-defined environment behaviour
  - exception handling print or raise for interactive or app use cases
  - number of significant digits for print can be set
  - user-defined preferred units can be defined for printing to reduce broilerplate code 

Some features of forallpeople e.g. prefixes, html and latex printing are not implemented. Weaknesses like handling °C and K units remain.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[//]: # ()
[//]: # (<!-- GETTING STARTED -->)

[//]: # (## Getting Started)

[//]: # ()
[//]: # (This is an example of how you may give instructions on setting up your project locally.)

[//]: # (To get a local copy up and running follow these simple example steps.)

[//]: # ()
[//]: # (### Prerequisites)

[//]: # ()
[//]: # (This is an example of how to list things you need to use the software and how to install them.)

[//]: # (* npm)

[//]: # (  ```sh)

[//]: # (  npm install npm@latest -g)

[//]: # (  ```)

[//]: # ()
[//]: # (### Installation)

[//]: # ()
[//]: # (1. Get a free API Key at [https://example.com]&#40;https://example.com&#41;)

[//]: # (2. Clone the repo)

[//]: # (   ```sh)

[//]: # (   git clone https://github.com/jkbgbr/simplesi.git)

[//]: # (   ```)

[//]: # (3. Install NPM packages)

[//]: # (   ```sh)

[//]: # (   npm install)

[//]: # (   ```)

[//]: # (4. Enter your API in `config.js`)

[//]: # (   ```js)

[//]: # (   const API_KEY = 'ENTER YOUR API';)

[//]: # (   ```)

[//]: # (5. Change git remote url to avoid accidental pushes to base project)

[//]: # (   ```sh)

[//]: # (   git remote set-url origin jkbgbr/simplesi)

[//]: # (   git remote -v # confirm the changes)

[//]: # (   ```)

[//]: # ()
[//]: # (<p align="right">&#40;<a href="#readme-top">back to top</a>&#41;</p>)

[//]: # ()
[//]: # ()
[//]: # ()
[//]: # (<!-- USAGE EXAMPLES -->)

[//]: # (## Usage)

[//]: # ()
[//]: # (Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.)

[//]: # ()
[//]: # (_For more examples, please refer to the [Documentation]&#40;https://example.com&#41;_)

[//]: # ()
[//]: # (<p align="right">&#40;<a href="#readme-top">back to top</a>&#41;</p>)

[//]: # ()
[//]: # ()
[//]: # ()
[//]: # (<!-- ROADMAP -->)

[//]: # (## Roadmap)

[//]: # ()
[//]: # (- [ ] Feature 1)

[//]: # (- [ ] Feature 2)

[//]: # (- [ ] Feature 3)

[//]: # (    - [ ] Nested Feature)

[//]: # ()
[//]: # (See the [open issues]&#40;https://github.com/jkbgbr/simplesi/issues&#41; for a full list of proposed features &#40;and known issues&#41;.)

[//]: # ()
[//]: # (<p align="right">&#40;<a href="#readme-top">back to top</a>&#41;</p>)

[//]: # ()
[//]: # ()
[//]: # ()
[//]: # (<!-- CONTRIBUTING -->)

[//]: # (## Contributing)

[//]: # ()
[//]: # (Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.)

[//]: # ()
[//]: # (If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".)

[//]: # (Don't forget to give the project a star! Thanks again!)

[//]: # ()
[//]: # (1. Fork the Project)

[//]: # (2. Create your Feature Branch &#40;`git checkout -b feature/AmazingFeature`&#41;)

[//]: # (3. Commit your Changes &#40;`git commit -m 'Add some AmazingFeature'`&#41;)

[//]: # (4. Push to the Branch &#40;`git push origin feature/AmazingFeature`&#41;)

[//]: # (5. Open a Pull Request)

[//]: # ()
[//]: # (<p align="right">&#40;<a href="#readme-top">back to top</a>&#41;</p>)

[//]: # ()
[//]: # (### Top contributors:)

[//]: # ()
[//]: # (<a href="https://github.com/jkbgbr/simplesi/graphs/contributors">)

[//]: # (  <img src="https://contrib.rocks/image?repo=jkbgbr/simplesi" alt="contrib.rocks image" />)

[//]: # (</a>)

[//]: # ()

<!-- LICENSE -->
## License

Distributed under the MIT. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

jkbgbr@gmail.com

[//]: # (Project Link: [https://github.com/jkbgbr/simplesi]&#40;https://github.com/jkbgbr/simplesi&#41;)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Connor Fester](https://github.com/connorferster)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
