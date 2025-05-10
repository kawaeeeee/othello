#!/bin/bash
cd backend
poetry install
cd ../frontend
npm install
cd ../
sleep infinity