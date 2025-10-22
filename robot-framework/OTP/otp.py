import pyotp
from robot.api.deco import keyword

class OTP:
	"""
		Library for generating One-Time Passwords (OTP) used in 2FA (Two-Factor Authentication).

		This class provides Robot Framework keywords for working with OTPs based on a shared secret.  
		Currently, it supports generating a TOTP (Time-based One-Time Password), 
		which is compatible with common authenticators such as Google Authenticator, Authy, etc.

		*Example:*
			\n`${otp}=    OTP.Get Otp    ${secret}`
			\n`Log    Your current OTP is: ${otp}`
	"""
	@staticmethod
	@keyword
	def get_otp(secret: str) -> int:
		"""Gets one time password for 2 factor authenticator.
		\n**Args:**
			\n- secret (str): secret returned by QR code.
		\n**Returns** (int): numeric value based off of secret given.
		"""
		totp = pyotp.TOTP(secret)
		return totp.now()
