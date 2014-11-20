STARTUP_SCRIPT = """\
sh /home/rbraunstein/run_docker &

# Sanity test for the startup script execution
mkdir /tmp/zomg/index.html && cd /tmp/zomg
echo 'commlink online' > index.html
python -m SimpleHTTPServer 9090 &
"""

def create_request(instance_name, disk_name):
  return {
    "disks": [
      {
        "type": "PERSISTENT",
        "boot": True,
        "mode": "READ_WRITE",
        "deviceName": disk_name,
        "autoDelete": False, # FIXME: for testing
        "source": "https://www.googleapis.com/compute/v1/projects/di-game-server/zones/us-central1-a/disks/" + disk_name
      }
    ],
    "networkInterfaces": [
      {
        "network": "https://www.googleapis.com/compute/v1/projects/di-game-server/global/networks/default",
        "accessConfigs": [
          {
            "name": "External NAT",
            "type": "ONE_TO_ONE_NAT"
          }
        ]
      }
    ],
    'metadata': [{
      'items': [{
        'key': 'startup-script',
        'value': STARTUP_SCRIPT
      },
      { #FIXME :add the metadata here (see also create page)
        'key': 'instance-name',
        'value': instance_name
      }
      ]
    }],
    "tags": {
      "items": []
    },
    "zone": "https://www.googleapis.com/compute/v1/projects/di-game-server/zones/us-central1-a",
    "canIpForward": False,
    "scheduling": {
      "automaticRestart": True,
      "onHostMaintenance": "MIGRATE"
    },
    "name": instance_name,
    "machineType": "https://www.googleapis.com/compute/v1/projects/di-game-server/zones/us-central1-a/machineTypes/n1-standard-1",
    "serviceAccounts": [
      {
        "email": "default",
        "scopes": [
          "https://www.googleapis.com/auth/userinfo.email",
          "https://www.googleapis.com/auth/compute.readonly",
          "https://www.googleapis.com/auth/devstorage.read_only"
        ]
      }
    ]
  }
