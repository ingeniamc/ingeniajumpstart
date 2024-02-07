@Library('cicd-lib@0.6') _

pipeline {
    agent none
    environment {
        HOME = '.'
    }
    stages {
        stage("Test") {
            agent {
                docker {
                    label 'windows-slave'
                    image 'ingeniacontainers.azurecr.io/win-python-builder:1.1'
                }
            }


            stages {
                stage("Install Dependencies") {
                    steps {
                        bat """
                            py -3.9 -m pipenv install -d --ignore-pipfile
                        """
                    }
                }
                stage("Code checks") {
                    parallel {
                        stage('Mypy') {
                            steps {
                                bat """
                                    py -3.9 -m pipenv run mypy ./k2basecamp --config-file mypy.ini --junit-xml=mypy_junit.xml
                                """
                            }
                            post {
                                always {
                                    junit "mypy_junit.xml"
                                }
                            }
                        }
                        stage("Formatting") {
                            steps {
                                bat """
                                    py -3.9 -m pipenv run black ./k2basecamp --check
                                """
                            }
                        }
                        stage("Linting") {
                            steps {
                                bat """
                                    py -3.9 -m pipenv run ruff ./k2basecamp --output-format=junit --output-file=ruff_junit.xml
                                """
                            }
                            post {
                                always {
                                    junit "ruff_junit.xml"
                                }
                            }
                        }
                        stage("QML Linting") {
                            steps {
                                bat """
                                    py -3.9 -m pipenv run pyside6-project build
                                """
                                bat """
                                    py -3.9 -m pipenv run qmllinting.py
                                """
                            }
                        }
                        
                    }
                }                
                stage("Tests") {
                    stages {
                        stage("Unit Tests") {
                            steps {
                                bat """
                                    py -3.9 -m pipenv run pytest ./tests/unit --junitxml=pytest_unit_junit.xml
                                """
                            }
                            post {
                                always {
                                    junit "pytest_unit_junit.xml"
                                }
                            }
                        }
                        stage("GUI Tests") {
                            steps {
                                bat """
                                    py -3.9 -m pipenv run pytest ./tests/gui --junitxml=pytest_gui_junit.xml
                                """
                            }
                            post {
                                always {
                                    junit "pytest_gui_junit.xml"
                                }
                            }
                        }

                    }
                }
                stage("Generate documentation") {
                    steps {
                        bat """
                            py -3.9 -m pipenv run python -m sphinx -b html docs/source _docs
                        """
                    }
                }
                stage('Archive') {
                    steps {
                        bat """
                            "C:\\Program Files\\7-Zip\\7z.exe" a -r docs.zip -w _docs -mem=AES256
                            XCOPY dist ${env.WORKSPACE}\\dist /i
                            XCOPY docs.zip ${env.WORKSPACE}
                        """
                        archiveArtifacts artifacts: "dist\\*, docs.zip"
                    }
                }
            }
        }
    }
}
