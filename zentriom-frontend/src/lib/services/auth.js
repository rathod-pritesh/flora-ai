import { API_URL } from '$lib/config/api';

function getToken() {
	const stored = localStorage.getItem('auth');

	if (!stored) return null;

	try {
		return JSON.parse(stored).token;
	} catch {
		return null;
	}
}

export function getAuthHeaders() {
	const token = getToken();

	return {
		'Content-Type': 'application/json',
		Authorization: `Bearer ${token}`
	};
}

export async function loginWithGoogle(idToken) {
	console.log('Sending token to backend');
	console.log(idToken.substring(0, 50));

	const response = await fetch(`${API_URL}/auth/google`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			token: idToken
		})
	});

	if (!response.ok) {
		throw new Error('Google login failed');
	}

	return await response.json();
}

export async function sendSignupOtp(name, email) {
	const response = await fetch(`${API_URL}/auth/signup/send-otp`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			name,
			email
		})
	});

	const data = await response.json();

	if (!response.ok) {
		throw new Error(data.detail || 'Failed to send verification code.');
	}

	return data;
}

export async function verifySignupOtp(email, otp) {
	const response = await fetch(`${API_URL}/auth/signup/verify-otp`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			email,
			otp
		})
	});

	const data = await response.json();

	if (!response.ok) {
		throw new Error(data.detail || 'OTP verification failed.');
	}

	return data;
}

export async function register(name, email, password) {
	const response = await fetch(`${API_URL}/auth/register`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			name,
			email,
			password
		})
	});

	const data = await response.json();

	if (!response.ok) {
		throw new Error(data.detail || 'Registration failed');
	}

	return data;
}

export async function login(email, password) {
	const response = await fetch(`${API_URL}/auth/login`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			email,
			password
		})
	});

	const data = await response.json();

	if (!response.ok) {
		throw new Error(data.detail || 'Login failed');
	}

	return data;
}

export async function forgotPassword(email) {
	const response = await fetch(`${API_URL}/auth/forgot-password`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			email
		})
	});

	const data = await response.json();

	if (!response.ok) {
		throw new Error(data.detail || 'Failed to send OTP');
	}

	return data;
}

export async function verifyOtp(email, otp) {
	const response = await fetch(`${API_URL}/auth/verify-otp`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			email,
			otp
		})
	});

	const data = await response.json();

	if (!response.ok) {
		throw new Error(data.detail || 'OTP verification failed');
	}

	return data;
}

export async function resetPassword(email, otp, password) {
	const response = await fetch(`${API_URL}/auth/reset-password`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			email,
			otp,
			password
		})
	});

	const data = await response.json();

	if (!response.ok) {
		throw new Error(data.detail || 'Password reset failed');
	}

	return data;
}

export async function explainCode(code) {
	const response = await fetch(`${API_URL}/code-explainer`, {
		method: 'POST',
		headers: getAuthHeaders(),
		body: JSON.stringify({
			code
		})
	});

	return await response.json();
}

export async function getHistory() {
	const response = await fetch(`${API_URL}/history`, {
		headers: getAuthHeaders()
	});

	if (!response.ok) {
		throw new Error('Failed to fetch history');
	}

	return await response.json();
}

export async function deleteHistory(id) {
	const response = await fetch(`${API_URL}/history/${id}`, {
		method: 'DELETE',
		headers: getAuthHeaders()
	});

	if (!response.ok) {
		throw new Error('Failed to delete history');
	}

	return await response.json();
}

export async function clearHistory() {
	const response = await fetch(`${API_URL}/history`, {
		method: 'DELETE',
		headers: getAuthHeaders()
	});

	if (!response.ok) {
		throw new Error('Failed to delete history');
	}

	return await response.json();
}

export async function sendChatMessage(prompt) {
	const response = await fetch(`${API_URL}/chat`, {
		method: 'POST',
		headers: getAuthHeaders(),
		body: JSON.stringify({ prompt })
	});

	if (!response.ok) {
		throw new Error('Failed to send chat message');
	}

	return await response.json();
}

export async function checkGrammar(text) {
	const response = await fetch(`${API_URL}/grammar`, {
		method: 'POST',
		headers: getAuthHeaders(),
		body: JSON.stringify({ text })
	});

	if (!response.ok) {
		throw new Error('Failed to check grammar');
	}

	return await response.json();
}

export async function generateLinkedInPost(payload) {
	const response = await fetch(`${API_URL}/linkedin`, {
		method: 'POST',
		headers: getAuthHeaders(),
		body: JSON.stringify(payload)
	});

	if (!response.ok) {
		throw new Error('Failed to generate LinkedIn post');
	}

	return await response.json();
}
