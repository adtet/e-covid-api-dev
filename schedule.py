import flask
import mysql.connector
from flask import Flask, jsonify, request
import uuid
import base64
import hashlib
import json
import datetime
from datetime import date
import calendar
from waitress import serve
app = Flask(__name__)
