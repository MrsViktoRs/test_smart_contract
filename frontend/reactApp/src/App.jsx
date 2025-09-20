import { useState } from "react";
import { ethers } from "ethers";
import "./App.css";
import contractData from "../../../backend/build/BaseContract.json";

function App() {
  const [account, setAccount] = useState(null);
  const [network, setNetwork] = useState(null);
  const [switchPrice, setSwitchPrice] = useState(false);
  const [gasPrice, setGasPrice] = useState(null);
  const [gasPriceETH, setGasPriceETH] = useState(null);

  const connectWallet = async () => {
    if (!window.ethereum) {
      alert("Установите MetaMask или TrustWallet в браузер");
      return;
    }

    const provider = new ethers.providers.Web3Provider(window.ethereum);
    await provider.send("eth_requestAccounts", []);
    const signer = provider.getSigner();

    const acc = await signer.getAddress();
    const net = await provider.getNetwork();

    let gp;
    try {
      gp = await provider.getGasPrice();
    } catch (e) {
      console.error("Не удалось получить цену газа", e);
      gp = ethers.BigNumber.from("0");
    }

    setAccount(acc);
    setNetwork(net.name);

    const gpGwei = Number(ethers.utils.formatUnits(gp, "gwei"));
    setGasPrice(gpGwei);

    const gpETH = Number(ethers.utils.formatUnits(gp, "ether"));
    setGasPriceETH(gpETH.toFixed(12));

    const contract = new ethers.Contract(
      contractData.address,
      contractData.abi,
      signer
    );

  };

  const switchPriceHandler = () => {
    setSwitchPrice(!switchPrice);
  };


  return (
    <div style={{ padding: 20, textAlign: "center"}}>
      <h1>Web3 dApp</h1>
      <button onClick={connectWallet}>Подключить TrustWallet</button>
      {account && (
        <div className="wallet-info">
          <p>Сеть: {network}</p>
          <p>Адрес: {account}</p>
          {switchPrice ? (
            <p onClick={switchPriceHandler} style={{cursor: "pointer"}}>Цена газа: {gasPriceETH} ETH</p>
          ): (
            <p onClick={switchPriceHandler} style={{cursor: "pointer"}}>Цена газа: {gasPrice} gwei</p>
          )}  
          
        </div>
      )}
    </div>
  );
}

export default App;
