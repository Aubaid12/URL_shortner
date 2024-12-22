import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import axios from 'axios';

function App() {
  const [url, setUrl] = useState("")
  const [shortned_url, setShortned_url] = useState("")
  
  const callbackend = async()=>{
    var response = await axios.get("http://localhost:5000/url_shortner", {params:{"url":url}})
    setShortned_url(response.data)
  } 
  


  return (
    <>
    <div className='Main'>
    <div className='left'>
    <h2>URL Shortner</h2>
    <img className='bg_image float' src='/hero.svg'/>
    </div>  
    <div className='form_outerbox'>
    <div className='form_box'>
    <input className='input_form' placeholder='Enter an URL' type = "text" onChange={(e)=>{setUrl(e.target.value)}}/>
    <button className='btn' onClick={callbackend} >short url</button>
    <div className='shortned'>{shortned_url}</div>
    </div> 
    </div>
    </div>
    </>
  );
}

export default App;
