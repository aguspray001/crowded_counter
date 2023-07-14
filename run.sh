#!/usr/bin/with-contenv bashio

echo "Start HCM Crowded Counter!"

# bashio::log.info "Bootnode address for this app => : $(echo -n "${BOOTNODE_ADDRESS}")"
# bashio::log.info "Bootnode address for this app => : $(echo -n "${BOOTNODE_PORT}")"

#execute main program
# npm run ws-dev
python main.py