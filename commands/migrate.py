from dotenv import load_dotenv
load_dotenv()
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from common.database import Base, engine
from models import *

Base.metadata.create_all(engine)