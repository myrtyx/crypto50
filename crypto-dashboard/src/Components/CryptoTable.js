// src/Components/CryptoTable.js
import React, { useEffect, useState } from 'react';

function CryptoTable() {
  const [data, setData] = useState([]);

  // Загрузка данных при монтировании компонента
  useEffect(() => {
    fetch('/api/data') // Заменить на правильный URL, если нужно
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error('Error fetching data:', error));
  }, []);

  const exchanges = ['Binance', 'Bybit', 'OKX'];

  // Функция для проверки наличия биржи и возврата стиля
  const getExchangeColor = (coin, exchange) => {
    return coin.CEX && coin.CEX.includes(exchange) ? 'green' : 'red';
  };

  const formatNumberWithSuffix = (number) => {
    if (number >= 1e12) {
      return (number / 1e12).toFixed(1) + 'T'; // Триллионы
    }
    if (number >= 1e9) {
      return (number / 1e9).toFixed(1) + 'B'; // Миллиарды
    }
    if (number >= 1e6) {
      return (number / 1e6).toFixed(1) + 'M'; // Миллионы
    }
    return number.toString();
  };

  const formatNumber = (number) => {
    if (number < 1) {
      // Преобразуем в строку и убираем лишние нули
      const numStr = number.toString();
  
      // Если количество значащих цифр после запятой меньше или равно 3, просто возвращаем это число
      const significantDigits = numStr.replace(/^0+|\./g, '').length;
      if (significantDigits <= 3) {
        return numStr;
      }
  
      // Если число имеет больше 3 значащих цифр, показываем до 3 значащих цифр после нуля
      return number.toPrecision(3);
    } else {
      // Если число больше или равно 1, оставляем два знака после запятой
      return number.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    }
  };

  return (
    <div>
      <h1>Crypto Dashboard</h1>
      <table border="1" cellPadding="5" cellSpacing="0">
        <thead>
          <tr>
            <th>FDV Rank</th>
            <th>Image</th>
            <th>Name</th>
            <th>Symbol</th>
            <th>Price</th>
            <th>Market Cap</th>
            <th>FDV</th>
            <th>CEX</th>
            <th>MC Rank</th>
          </tr>
        </thead>
        <tbody>
          {data.length > 0 ? (
            data.map((coin) => (
              <tr key={coin.Rank}>
                <td>{coin.Rank}</td>
                <td>
                  <img src={coin.Image} alt={coin.Name} width="40" height="40" />
                </td>
                <td>{coin.Name}</td>
                <td>{coin.Symbol}</td>
                <td>{formatNumber(coin.Price)}$</td>
                <td>{formatNumberWithSuffix(coin.MarketCap)}$</td>
                <td>{formatNumberWithSuffix(coin.FDV)}$</td>
                <td>
                  {exchanges.map((exchange, index) => (
                    <span
                      key={index}
                      style={{
                        color: getExchangeColor(coin, exchange),
                        marginRight: '5px'
                      }}
                    >
                      {exchange}
                    </span>
                  ))}
                </td>
                <td>{coin['M Rank']}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="9">Данные не найдены</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default CryptoTable;
