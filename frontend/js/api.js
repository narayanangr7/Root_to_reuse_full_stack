class ApiService {
    constructor() {
        // In production (Vercel), use relative /api path so Vercel routes it to the serverless function.
        // In local development, fall back to localhost:8000.
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            this.baseUrl = 'http://127.0.0.1:8000';
        } else {
            this.baseUrl = '/api';
        }
    }

    async request(endpoint, method = 'GET', body = null, requiresAuth = false) {
        const url = `${this.baseUrl}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
        };

        if (requiresAuth) {
            // const token = localStorage.getItem('token');
            // if (token) {
            //     headers['Authorization'] = `Bearer ${token}`;
            // }
        }

        const config = {
            method,
            headers,
        };

        if (body) {
            config.body = JSON.stringify(body);
        }

        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'API Request failed');
            }
            return await response.json();
        } catch (error) {
            console.error(`API Error (${method} ${endpoint}):`, error);
            throw error;
        }
    }

    get(endpoint, requiresAuth = false) {
        return this.request(endpoint, 'GET', null, requiresAuth);
    }

    post(endpoint, data, requiresAuth = false) {
        return this.request(endpoint, 'POST', data, requiresAuth);
    }

    put(endpoint, data, requiresAuth = false) {
        return this.request(endpoint, 'PUT', data, requiresAuth);
    }

    delete(endpoint, requiresAuth = false) {
        return this.request(endpoint, 'DELETE', null, requiresAuth);
    }
}

const api = new ApiService();
