// src/Components/CryptoTable.js
import React, { useEffect, useState } from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import { Container } from '@mui/material';

function CryptoTable() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/api/data') // Заменить на правильный URL
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error('Error fetching data:', error));
  }, []);

  const exchanges = ['Binance', 'Bybit', 'OKX'];

  const getExchangeColor = (coin, exchange) => {
    return coin.CEX && coin.CEX.includes(exchange) ? 'green' : 'red';
  };

  const formatNumberWithSuffix = (number) => {
    if (number >= 1e12) return (number / 1e12).toFixed(1) + 'T';
    if (number >= 1e9) return (number / 1e9).toFixed(1) + 'B';
    if (number >= 1e6) return (number / 1e6).toFixed(1) + 'M';
    return number.toString();
  };

  const formatNumber = (number) => {
    if (number < 1) {
      const numStr = number.toString();
      const significantDigits = numStr.replace(/^0+|\./g, '').length;
      return significantDigits <= 3 ? numStr : number.toPrecision(3);
    }
    return number.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  };

  return (
    <Box sx={{ textAlign: 'center', padding: '50px', marginBottom: '60px' }}>
      <Typography
        variant='h1'
        sx={{ 
          fontSize: '3rem', 
          color: '#56b1bf', 
          marginBottom: '30px'
        }}
        >
        Crypto Dashboard
      </Typography>
      
      <TableContainer component={Paper} sx={{
        margin: '20px auto',
        maxWidth: '1250px',
        borderRadius: '8px',
        overflow: 'hidden',
        boxShadow: '0 3px 3px #56b1bf',
      }}>
        <Table>
          <TableHead>
            <TableRow>
              {['FDV #', '', 'Name', 'Symbol', 'Price', 'Market Cap', 'FDV', 'CEX', 'MC #'].map((header) => (
                <TableCell
                  key={header}
                  sx={{
                    backgroundColor: '#56b1bf',
                    color: '#ffffff',
                    padding: '16px',
                    fontSize: '1rem',
                    textAlign: 'center'
                  }}
                >
                  {header}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {data.length > 0 ? (
              data.map((coin) => (
                <TableRow
                  key={coin.Rank}
                  sx={{
                    transition: 'background-color 0.2s',
                    '&:nth-of-type(even)': { backgroundColor: '#f8f8f8' },
                    '&:hover': { backgroundColor: '#f3f7fa' },
                  }}
                >
                  <TableCell sx={{ padding: '12px', borderBottom: '1px solid #ddd', fontSize: '0.95rem', textAlign: 'center' }}>{coin.Rank}</TableCell>
                  <TableCell sx={{ padding: '12px', borderBottom: '1px solid #ddd', fontSize: '0.95rem', textAlign: 'center' }}>
                    <Avatar src={coin.Image} alt={coin.Name} sx={{ width: 40, height: 40 }} />
                  </TableCell>
                  <TableCell sx={{ padding: '12px', borderBottom: '1px solid #ddd', fontSize: '0.95rem', textAlign: 'center' }}>{coin.Name}</TableCell>
                  <TableCell sx={{ padding: '12px', borderBottom: '1px solid #ddd', fontSize: '0.95rem', textAlign: 'center' }}>{coin.Symbol}</TableCell>
                  <TableCell sx={{ padding: '12px', borderBottom: '1px solid #ddd', fontSize: '0.95rem', textAlign: 'right' }}>$ {formatNumber(coin.Price)}</TableCell>
                  <TableCell sx={{ padding: '12px', borderBottom: '1px solid #ddd', fontSize: '0.95rem', textAlign: 'right' }}>$ {formatNumberWithSuffix(coin.MarketCap)}</TableCell>
                  <TableCell sx={{ padding: '12px', borderBottom: '1px solid #ddd', fontSize: '0.95rem', textAlign: 'right' }}>$ {formatNumberWithSuffix(coin.FDV)}</TableCell>
                  <TableCell sx={{ padding: '12px', borderBottom: '1px solid #ddd', fontSize: '0.95rem', textAlign: 'center' }}>
                    {exchanges.map((exchange, index) => (
                      <Typography
                        key={index}
                        component="span"
                        sx={{
                          color: getExchangeColor(coin, exchange),
                          marginRight: '8px',
                          fontWeight: 500
                        }}
                      >
                        {exchange}
                      </Typography>
                    ))}
                  </TableCell>
                  <TableCell sx={{ padding: '12px', borderBottom: '1px solid #ddd', fontSize: '0.95rem', textAlign: 'center' }}>{coin['M Rank']}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={9} align="center">
                  <Typography variant="body1" color="textSecondary">
                    Данные не найдены
                  </Typography>
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default CryptoTable;