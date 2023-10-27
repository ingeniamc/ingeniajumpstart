@Library('cicd-lib@0.6') _

pipeline {
    agent none
    environment {
        HOME = '.'
    }
    stages {
        stage("Test") {
            agent {
                label {
                    label "worker"
                    docker "python:3.11.4"
                }
            }
            stages {
                stage("Install Dependencies") {
                    steps {
                        sh "pip install pipenv"
                        sh "pipenv install -d --ignore-pipfile"
                    }
                }
                stage("Code checks") {
                    parallel {
                        stage("Formatting") {
                            steps {
                                sh "pipenv run black ./src --check"
                            }
                        }
                        stage("Linting") {
                            steps {
                                sh "pipenv run ruff ./src --output-format=junit --output-file=ruff_junit.xml"
                            }
                            post {
                                always {
                                    junit "backend/ruff_junit.xml"
                                }
                            }
                        }
                        stage("QML Linting") {
                            steps {
                                sh "pipenv run pyside6-project build"
                                sh "pipenv run qmllinting.py"
                            }
                        }
                        stage("Type Checking") {
                            steps {
                                sh "pipenv run mypy ./src --config-file mypy.ini --junit-xml=mypy_junit.xml"
                            }
                            post {
                                always {
                                    junit "mypy_junit.xml"
                                }
                            }
                        }
                    }
                }                
                stage("Tests") {
                    stages {
                        stage("Unit Tests") {
                            steps {
                                sh "pipenv run pytest ./src/tests/unit --junitxml=pytest_unit_junit.xml"
                            }
                            post {
                                always {
                                    junit "pytest_unit_junit.xml"
                                }
                            }
                        }
                        stage("GUI Tests") {
                            steps {
                                sh "pipenv run pytest ./src/tests/gui --junitxml=pytest_gui_junit.xml"
                            }
                            post {
                                always {
                                    junit "pytest_gui_junit.xml"
                                }
                            }
                        }

                    }
                }
            }
            post {
                always {
                    cleanWs()
                }
            }
        }
    }
}
