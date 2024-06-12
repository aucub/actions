#!/bin/bash

# 安装所需的程序
sudo apt-get update
sudo apt-get install -y curl wireguard resolvconf

curl ifconfig.me

# 下载并配置订阅文件
SUBSCRIPTION_URL="https://warp-clash-api-e5ga.onrender.com/api/wireguard?best=false&randomName=true&proxyFormat=full&ipv6=false"
wget $SUBSCRIPTION_URL -O ~/wg0.conf

# 获取默认网关和公网IP地址
GATEWAY_IP=$(ip route get 8.8.8.8 | awk '{print $3}' | head -n 1)
PUBLIC_IP=$(ip -brief address show eth0 | awk '{print $4}' | cut -d '/' -f 1)

# 检查 IP 地址和网关是否有效
if [ -z "$GATEWAY_IP" ] || [ -z "$PUBLIC_IP" ]; then
    echo "无法获取默认网关或公网 IP 地址。请检查网络配置。"
    exit 1
fi

# 将IP地址和网关添加到配置文件
sed -i "/\[Interface\]/a PostUp = ip rule add table 200 from $PUBLIC_IP\nPostUp = ip route add table 200 default via $GATEWAY_IP\nPreDown = ip rule delete table 200 from $PUBLIC_IP\nPreDown = ip route delete table 200 default via $GATEWAY_IP" ~/wg0.conf

# 将配置文件移动到/etc/wireguard/目录
sudo mv ~/wg0.conf /etc/wireguard/

# 创建 WireGuard 服务文件
cat <<EOF | sudo tee /etc/systemd/system/wg-quick@wg0.service
[Unit]
Description=WireGuard via wg-quick(8) for wg0
After=network-online.target nss-lookup.target
Wants=network-online.target nss-lookup.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/bin/wg-quick up wg0
ExecStop=/usr/bin/wg-quick down wg0
ExecReload=/usr/bin/wg-quick down wg0
ExecReload=/usr/bin/wg-quick up wg0

[Install]
WantedBy=multi-user.target
EOF

# 启动WireGuard服务
sudo systemctl daemon-reload
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0

curl ifconfig.me
