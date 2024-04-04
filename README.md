# Technical Test - Connect Think Internship
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue) ![GIT](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white) ![Markdown](https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white) ![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white) ![scikit-learn](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)


## Overview
The project consists of a Jupyter notebook where a classification algorithm is developed to determine the quality of wine based on certain wine characteristics. Additionally, an application is built where the user can obtain a summary according to the pages assigned from the following nutrition book: https://pressbooks.oer.hawaii.edu/humannutrition2/ 
<p align="center">
  <img src="app.png" alt="Sample Image" width="600">
</p>

## Setup Instructions
1. Clone the Repository:
    ```html
    git clone https://github.com/despinoza119/EDA_and_NLP_test.git
    ```

2. Define the necessary environment variables:
    ```html
    AZURE_DEPLOYMENT=
    AZURE_API_KEY=
    AZURE_ENDPOINT=
    ```

3. Build the docker image:
    ```html
    docker build -t nlp_test .
    ```

4. Run the docker image builded:
    ```html
    docker run -p 8501:8501 nlp_test
    ```

5. To visualize the app go to http://localhost:8501 :
    ```html
    http://localhost:8501
    ```

## Documentation
For more detailed information about the project overview, data model, and specific components, refer to the docs directory.

- **internship-test**: Instructions for building the project.

## License
MIT License