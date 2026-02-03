# E-Commerce API Architecture

A production-ready, scalable RESTful API built with **Django REST Framework** featuring modular architecture, Redis caching, multiple payment integrations, and containerized deployment.

---

## 🎯 Project Overview

This is a comprehensive e-commerce backend API designed with enterprise-level architecture principles. It demonstrates advanced Django patterns, microservices-ready design, and best practices in API development suitable for real-world deployment.

**Key Highlights:**
- Modular, scalable architecture with 6 independent Django apps
- JWT-based authentication with token blacklisting
- Redis-powered caching layer for high performance
- Multi-gateway payment processing (Stripe, SSLCommerz)
- Async task processing with Celery
- Complete Docker containerization for production deployment

---

## ✨ Key Features

### Core Functionality
- ✅ **User Authentication & Authorization** - JWT tokens with refresh capability and token blacklisting
- ✅ **Product Catalog** - Hierarchical categories with inventory tracking
- ✅ **Shopping Cart** - Redis-backed cart with real-time synchronization
- ✅ **Order Management** - Complete order lifecycle from creation to fulfillment
- ✅ **Payment Processing** - Integrated payment gateways (Stripe, SSLCommerz)
- ✅ **Async Operations** - Background tasks for emails, invoices, and stock updates via Celery
- ✅ **API Documentation** - Auto-generated interactive Swagger/OpenAPI specs

### Technical Architecture
- 📦 **Feature-Based Modular Structure** - Each feature is an independent Django app for scalability
- 🔒 **Enterprise Security** - CSRF protection, JWT authentication, permission-based access control
- ⚡ **High Performance** - Redis caching for frequently accessed data and sessions
- 📊 **Auto Documentation** - drf-yasg integration for interactive API exploration
- 🐳 **Container-Ready** - Docker & Docker Compose for consistent development and production environments
- 🧪 **Test Coverage** - Unit and integration tests for reliability

---

## 🏗️ Architecture Overview

### System Design
```
┌────────────────────────────────────────────────────────┐
│              Client Applications (Web/Mobile)          │
└─────────────────────┬────────────────────────────────┘
                      │ HTTPS
┌─────────────────────▼────────────────────────────────┐
│         Django REST API Gateway & Router             │
│    (Authentication, Permissions, Rate Limiting)      │
└────┬──────┬────────┬─────────┬──────────┬──────────┘
     │      │        │         │          │
  Users  Products  Orders   Cart      Payments
   Mgmt   Service  Service  Service   Service
     │      │        │         │          │
     └──────┴────────┴─────────┴──────────┘
              │
┌─────────────▼────────────────────────────────────┐
│         PostgreSQL Database Layer                 │
│  (Users, Products, Orders, Payments, History)   │
└──────────────────────────────────────────────────┘

┌──────────────┐  ┌─────────────┐  ┌────────────┐
│ Redis Cache  │  │   Celery    │  │  RabbitMQ  │
│ (Sessions,   │  │  Workers    │  │   Queue    │
│  Cart, TTL)  │  │ (Async Jobs)│  │            │
└──────────────┘  └─────────────┘  └────────────┘
```

### Module Responsibilities

| Module | Purpose | Key Models |
|--------|---------|-----------|
| **users** | User authentication & profiles | User, UserProfile, Tokens |
| **products** | Product catalog management | Product, Category, Inventory |
| **orders** | Order processing & tracking | Order, OrderItem |
| **payments** | Payment gateway integration | PaymentTransaction |
| **cart** | Shopping cart (Redis-backed) | Cart Sessions |
| **core** | Shared utilities & base classes | Exceptions, Pagination, Mixins |

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+
- Redis server (for caching and cart)
- PostgreSQL (recommended for production) or SQLite (development)
- Docker & Docker Compose (optional, for containerized deployment)
- pip and virtualenv

### Development Setup (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/E-commerce-API-Architecture.git
cd E-commerce-API-Architecture

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create superuser for admin panel
python manage.py createsuperuser

# 6. Start development server
python manage.py runserver
```

**Access the application:**
- 🌐 API Endpoints: http://localhost:8000/api/
- 📖 Swagger Documentation: http://localhost:8000/api/docs/
- 🔑 Admin Dashboard: http://localhost:8000/admin/

### Production Deployment (Docker)

```bash
# Build and run all services
docker-compose -f docker/docker-compose.yml up --build

# Run migrations in container
docker-compose -f docker/docker-compose.yml exec web python manage.py migrate

# Create superuser in container
docker-compose -f docker/docker-compose.yml exec web python manage.py createsuperuser

# Access running services
# API: http://localhost:8000/api/
# Admin: http://localhost:8000/admin/
# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

---

## 📚 API Endpoints Reference

### Authentication Endpoints
```
POST   /api/auth/register/          Register new user
POST   /api/auth/login/             Obtain JWT tokens
POST   /api/auth/refresh/           Refresh access token
POST   /api/auth/logout/            Invalidate token (blacklist)
GET    /api/auth/profile/           Get current user profile
```

### Product Endpoints
```
GET    /api/products/               List all products (paginated)
POST   /api/products/               Create new product (admin only)
GET    /api/products/{id}/          Get product details
PUT    /api/products/{id}/          Update product (admin only)
DELETE /api/products/{id}/          Delete product (admin only)
GET    /api/categories/             List all categories
GET    /api/categories/{id}/        Category details with products
```

### Order Endpoints
```
GET    /api/orders/                 List user's orders
POST   /api/orders/                 Create new order
GET    /api/orders/{id}/            Get order details & items
PUT    /api/orders/{id}/            Update order status (admin)
DELETE /api/orders/{id}/            Cancel order
GET    /api/orders/{id}/invoice/    Generate order invoice
```

### Cart Endpoints
```
GET    /api/cart/                   View current cart
POST   /api/cart/add/               Add item to cart
PUT    /api/cart/items/{id}/        Update item quantity
DELETE /api/cart/items/{id}/        Remove item from cart
POST   /api/cart/checkout/          Convert cart to order
POST   /api/cart/clear/             Clear entire cart
```

### Payment Endpoints
```
POST   /api/payments/process/       Initialize payment
POST   /api/payments/webhook/       Payment gateway webhook
GET    /api/payments/{id}/          Payment status & details
POST   /api/payments/{id}/verify/   Verify payment
```

---

## 🔧 Technology Stack

### Backend & Framework
- **Django 3.2+** - Web framework
- **Django REST Framework** - REST API toolkit
- **djangorestframework-simplejwt** - JWT authentication
- **drf-yasg** - Swagger/OpenAPI documentation generator
- **django-filter** - Advanced filtering for list endpoints

### Database & Caching
- **PostgreSQL** - Primary database (production)
- **SQLite** - Development database
- **Redis** - Session management, cart storage, rate limiting
- **Celery** - Distributed task queue

### Payment Integration
- **Stripe API** - Payment processing
- **SSLCommerz API** - Local payment gateway

### Deployment & DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Gunicorn** - WSGI application server
- **Nginx** - Reverse proxy & static file serving

### Development Tools
- **pytest** - Testing framework
- **Pillow** - Image processing
- **black** - Code formatting

---

## 🔐 Security Implementation

✅ **JWT Authentication** - Stateless token-based authentication  
✅ **Token Blacklisting** - Logout invalidates tokens immediately  
✅ **CSRF Protection** - Cross-Site Request Forgery prevention  
✅ **Permission Classes** - Fine-grained access control per endpoint  
✅ **Input Validation** - Serializer-based validation for all inputs  
✅ **Rate Limiting** - Request throttling to prevent abuse  
✅ **SQL Injection Prevention** - ORM parametrized queries  
✅ **CORS Configuration** - Controlled cross-origin resource sharing  
✅ **Secure Headers** - Security middleware for HTTP headers  

---

## 📊 Database Models

### User Model (Extended Django User)
```python
- id, email, username, password
- first_name, last_name, phone
- is_active, is_staff, is_superuser
- date_joined, last_login
```

### Product Model
```python
- id, name, description, category
- price, cost_price, discount_percentage
- stock_quantity, sku
- image_url, is_active
- created_at, updated_at
```

### Order Model
```python
- id, user (FK), order_number, status
- total_price, tax_amount, shipping_cost
- shipping_address, billing_address
- payment_method, payment_status
- created_at, updated_at, delivered_at
```

### Cart Model (Redis)
```python
- cart_key: user:{user_id}
- data: {product_id: quantity, ...}
- expiration: 30 days of inactivity
```

---

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users

# Run with verbosity
python manage.py test --verbosity=2

# With coverage report
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Test Coverage
- User authentication and permissions
- Product CRUD operations
- Order processing workflow
- Payment transaction handling
- Cart operations
- API response validations

---

## 📈 Performance Optimization

- **Database Indexing**: Foreign keys and common filter fields indexed
- **Query Optimization**: `select_related()` and `prefetch_related()` to prevent N+1 queries
- **Pagination**: Default pagination (20 items/page) for list endpoints
- **Redis Caching**: 
  - Cart data (TTL: 30 days)
  - User sessions (TTL: 24 hours)
  - Frequently accessed products (TTL: 1 hour)
- **Async Task Processing**: Long-running operations (emails, PDF generation) via Celery
- **Connection Pooling**: Database connection reuse via connection pools

---

## 🚢 Production Deployment Checklist

### Configuration
- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure `ALLOWED_HOSTS` with actual domains
- [ ] Update `SECRET_KEY` to a secure random value
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure environment variables properly

### Security
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure CORS for trusted domains only
- [ ] Set up API rate limiting
- [ ] Enable security middleware headers
- [ ] Configure database backups and replication

### Scaling
- [ ] Set up load balancing (Nginx/HAProxy)
- [ ] Configure Redis for clustering
- [ ] Enable Celery worker scaling
- [ ] Implement database read replicas
- [ ] Set up CDN for static files

### Monitoring
- [ ] Enable application logging
- [ ] Set up error tracking (Sentry)
- [ ] Monitor API performance metrics
- [ ] Configure database monitoring
- [ ] Set up alerting for critical issues

---

## 📂 Project Structure

```
E-commerce-API-Architecture/
│
├── ecommerce/                  # Project configuration
│   ├── settings.py            # Django settings
│   ├── urls.py                # URL routing
│   ├── wsgi.py                # WSGI configuration
│   └── asgi.py                # ASGI configuration
│
├── users/                      # User & authentication
│   ├── models.py              # User models
│   ├── serializers.py         # API serializers
│   ├── views.py               # API views
│   ├── urls.py                # User routes
│   └── services/
│       └── auth_service.py    # Auth business logic
│
├── products/                   # Product management
│   ├── models.py              # Product, Category models
│   ├── serializers.py         # Product serializers
│   ├── views.py               # Product viewsets
│   ├── urls.py                # Product routes
│   └── services/
│       └── inventory_service.py
│
├── orders/                     # Order processing
│   ├── models.py              # Order, OrderItem models
│   ├── serializers.py         # Order serializers
│   ├── views.py               # Order viewsets
│   ├── urls.py                # Order routes
│   └── signals.py             # Order signals
│
├── payments/                   # Payment processing
│   ├── models.py              # Payment models
│   ├── views.py               # Payment views
│   ├── urls.py                # Payment routes
│   └── services/
│       ├── stripe_service.py  # Stripe integration
│       └── sslcommerz_service.py  # SSLCommerz integration
│
├── cart/                       # Shopping cart
│   ├── models.py
│   ├── views.py               # Cart operations
│   ├── serializers.py         # Cart serializers
│   ├── urls.py                # Cart routes
│   └── redis_client.py        # Redis operations
│
├── core/                       # Shared utilities
│   ├── utils.py               # Helper functions
│   ├── exceptions.py          # Custom exceptions
│   ├── pagination.py          # Pagination classes
│   └── mixins.py              # Mixin classes
│
├── docker/
│   ├── Dockerfile             # Application container
│   ├── docker-compose.yml     # Multi-container setup
│   └── nginx.conf             # Nginx configuration
│
├── static/                     # Static files (admin, DRF)
├── media/                      # User-uploaded files
├── manage.py
├── requirements.txt            # Python dependencies
├── postman_collection.json     # API test collection
└── README.md                   # This file
```

---

## 🤝 Development Workflow

### Adding a New Feature

1. **Create migrations if changing models**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Implement model, serializer, viewset, and URLs**

3. **Write tests**
   ```bash
   python manage.py test app_name
   ```

4. **Test API with Postman** (use postman_collection.json)

5. **Verify documentation** at `/api/docs/`

---

## 📞 Support & Documentation

- 📖 **Full API Documentation**: Access at `/api/docs/` (Swagger UI)
- 📝 **Postman Collection**: Import `postman_collection.json` for testing
- 🐛 **Issue Tracking**: GitHub Issues
- 💬 **Questions**: Open a discussion on GitHub

---

## 📋 Future Enhancements

- [ ] Implement product reviews and ratings
- [ ] Add wishlist functionality
- [ ] Email notifications for order updates
- [ ] Admin dashboard analytics
- [ ] Multi-language support (i18n)
- [ ] Advanced search with Elasticsearch
- [ ] Real-time notifications with WebSockets
- [ ] Mobile app OAuth integration

---

## 📝 License

This project is licensed under the MIT License. See LICENSE file for details.

---

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Guide](https://www.django-rest-framework.org/)
- [JWT Authentication Best Practices](https://tools.ietf.org/html/rfc7519)
- [Redis Caching Patterns](https://redis.io/topics/patterns)
- [Docker & Kubernetes](https://www.docker.com/get-started)
- [RESTful API Design](https://restfulapi.net/)

---

**Built with ❤️ using Django REST Framework**

*Last Updated: February 2026*
