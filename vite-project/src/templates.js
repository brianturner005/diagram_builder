const TEMPLATES = [
  {
    id: 'home-network',
    name: 'Home Network',
    icon: '🏠',
    description:
      'A home network with a broadband modem, WiFi router, smart TV, desktop PC, two laptops, a NAS for file storage, and smartphones connected wirelessly',
  },
  {
    id: '3-tier-web',
    name: '3-Tier Web App',
    icon: '🌐',
    description:
      'A three-tier web application with a load balancer, three web servers, three application servers, and a PostgreSQL database cluster with a primary and two replica nodes',
  },
  {
    id: 'aws-vpc',
    name: 'AWS VPC',
    icon: '☁️',
    description:
      'An AWS VPC with public and private subnets, internet gateway, NAT gateway, EC2 instances behind an Application Load Balancer, RDS database, ElastiCache, S3 bucket, and CloudFront CDN',
  },
  {
    id: 'corporate-office',
    name: 'Corporate Office',
    icon: '🏢',
    description:
      'A corporate office network with internet access through a firewall, core router, distribution switches, access switches for two floors with desktop PCs and laptops, and a server room with file servers, email server, and a database',
  },
  {
    id: 'dmz',
    name: 'DMZ Architecture',
    icon: '🔒',
    description:
      'A DMZ network security architecture with an external firewall facing the internet, a DMZ zone containing a reverse proxy and web servers, an internal firewall, and a protected internal zone with application servers and databases',
  },
  {
    id: 'kubernetes',
    name: 'Kubernetes Cluster',
    icon: '⚙️',
    description:
      'A Kubernetes cluster with a control plane containing the API server, etcd, scheduler, and controller manager, three worker nodes each running application pods, an ingress controller, and persistent volume storage',
  },
  {
    id: 'azure-app',
    name: 'Azure App Service',
    icon: '🔷',
    description:
      'An Azure architecture with an API Management gateway, App Service hosting a web app, Azure Functions for background processing, Cosmos DB, Azure SQL Database, Blob Storage, Service Bus for messaging, and a VNet',
  },
  {
    id: 'gcp-data',
    name: 'GCP Data Pipeline',
    icon: '📊',
    description:
      'A GCP data pipeline with Cloud Load Balancing, Compute Engine instances, Cloud Pub/Sub for event streaming, Cloud Functions for processing, BigQuery for analytics, Cloud Storage for raw data, and Cloud SQL for transactional data',
  },
]

export default TEMPLATES
