from flask import Flask, render_template
import braintree
from app import app 
import os


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id = os.environ.get("merchant_id"),
        private_key = os.environ.get("private_key"),
        public_key = os.environ.get("public_key"),
        
    )
)


   