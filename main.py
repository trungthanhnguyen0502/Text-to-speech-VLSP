from typing import Optional
from datetime import datetime, timedelta
import logging
import os
import sys
from importlib import reload
import librosa
from scipy.io.wavfile import write

sys.path.append("tacotron2")
sys.path.append("tacotron2/waveglow")

from fastapi import FastAPI, HTTPException, status, Depends, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import uuid

from helpers import to_speech, load_tacotron, load_waveglow
import base64

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

user = {
    "email": "admin@sun-asterisk.com",
    "password": "72landmark",
}


class InputData(BaseModel):
    input_text: str
    voice: Optional[str] = None
    rate: Optional[float] = None
    output_type: Optional[str] = None


hparams, tacotron = load_tacotron()
waveglow, denoiser = load_waveglow(hparams)
os.makedirs(hparams.audio_outdir, exist_ok=True)
print("** loading model Okie !!! ")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(user, username: str, password: str):
    if not username == user["email"]:
        return False
    hashed_password = get_password_hash(user["password"])
    if not verify_password(password, hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_info = authenticate_user(user, form_data.username, form_data.password)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_info["email"]}, expires_delta=access_token_expires
    )

    return {"status": 1, "result": {"access_token": access_token}}


@app.post("/tts")
async def text_to_speech(data: InputData, access_token: Optional[str] = Header(None)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email == user["email"]:
            text = data.input_text
            
            audio = to_speech(text, tacotron, waveglow, denoiser, hparams)
            filename = "{}/{}.wav".format(hparams.audio_outdir, str(uuid.uuid4()))
        
            write(filename, rate=22050, data=audio)
            encode_string = base64.b64encode(open(filename, "rb").read())
            return {"status": 1, "result": {"data":encode_string}}
        else:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
