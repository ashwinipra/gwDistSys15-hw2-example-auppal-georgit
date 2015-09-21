#!/bin/sh
python convServer.py 5570 ft m &
python convServer.py 5571 m ft &
java ConvServer      5572 ft in 12.0 &
# python convServer.py 5572 ft in &
python convServer.py 5573 in ft &
java ConvServer      5574 ft in 2.54 &
# python convServer.py 5574 in cm &
python convServer.py 5575 cm in &
python convServer.py 5576 b m &
python convServer.py 5577 m b &
python convServer.py 5578 b y &
python convServer.py 5579 y b &
python convServer.py 5580 y $ &
python convServer.py 5581 $ y &
python convServer.py 5582 b kg &
python convServer.py 5583 kg b &
python convServer.py 5584 kg lbs &
java ConvServer      5585 lbs kg 0.45359237 &
# python convServer.py 5585 lbs kg &
python convServer.py 5586 lbs g &
python convServer.py 5587 g lbs &

# Start the proxy server
python proxy_conv_server.py 5555 conversion_servers.txt
