# Hydra Analytics Regulatory Compliance Intelligence Platform

## Overview

This project is an AI-powered Regulatory Compliance Intelligence Platform built for Hydra Analytics. It uses Retrieval-Augmented Generation to support semantic legal search, compliance question answering, regulatory summarisation, and source-traceable legal intelligence

## Business Problem

Hydra Analytics faced slow legal research, fragmented regulatory documents, inconsistent compliance interpretation, and delayed review cycles.

## Solution

The platform ingests legal documents, cleans the text, splits documents into semantic chunks, generates Hugging Face embeddings, stores vectors in Pinecone, retrieves relevant sources, and supports compliance-focused AI responses through FastAPI endpoints.

## Technology Stack

- Python
- FastAPI
- Pinecone
- Hugging Face Sentence Transformers
- LangChain text splitting
- Pydantic
- Pytest

## API Endpoints

- GET `/`
- GET `/health`
- POST `/search`
- POST `/qa`
- POST `/summarize`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
