import './Background.css'
import video1 from '../../Assets/video1.mp4'
import image1 from '../../Assets/image4.jpg'
import image2 from '../../Assets/image5.jpg'
import image3 from '../../Assets/image6.jpg'

const Background = ({playStatus,heroCount}) => {

    if (playStatus) {
        return (
            <video className='background fade-in' autoPlay loop muted>
                <source src={video1} type='video/mp4' />
            </video>
        )
    }
    else if(heroCount===0)
    {
        return <img src={image1} className='background fade-in' alt="" />
    }
    else if(heroCount===1)
    {
        return <img src={image2} className='background2 fade-in' alt="" />
    }
    else if(heroCount===2)
    {
        return <img src={image3} className='background3 fade-in' alt="" />
    }
}


export default Background
