@echo off
set PYFILE=%~f0
set PYFILE=%PYFILE:~0,-4%
"%~f0\..\..\python.exe" "%PYFILE%" %*