data "template_file" "user_data" {
  template = file("${path.module}/user-data.sh")
}

resource "digitalocean_ssh_key" "default" {
  name = "Abhishek SSH Key"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "digitalocean_droplet" "server" {
  image = "docker-18-04"
  name = "server"
  region = "nyc3"
  size = "s-1vcpu-2gb"

  monitoring = true
  private_networking = true

  user_data = data.template_file.user_data.rendered

  ssh_keys = [
    digitalocean_ssh_key.default.fingerprint]
}

resource "digitalocean_volume" "pg-data-vol" {
  name = "postgres_data"
  region = "nyc3"
  size = 10
  initial_filesystem_type = "xfs"
  initial_filesystem_label = "pg-data-vol"
}

resource "digitalocean_volume_attachment" "pg-data-vol-attachment" {
  droplet_id = digitalocean_droplet.server.id
  volume_id = digitalocean_volume.pg-data-vol.id
}

output "server_ip_addr" {
  value = digitalocean_droplet.server.ipv4_address
  description = "IP Address of the created Server"
}
