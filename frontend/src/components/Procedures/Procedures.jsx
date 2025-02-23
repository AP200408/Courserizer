import React from 'react';
import Latex from 'react-latex';
import 'katex/dist/katex.min.css'; // required for KaTeX styling
import Navbar from '../Navbar/Navbar';
import "./Procedures.css";
import Footer from '../Footer/Footer';

const Procedures = () => {
  return (
    <>
      <Navbar />
      <div className="container">
        <div className="latex-part">
          <h1 style={{textDecoration:"underline", textUnderlineOffset:"0.3em"}}>Metrics for Course Evaluation: A Comprehensive Report</h1>
          
          <section className="section">
            <h2>Overview</h2>
            <p>
              This section proposes a set of metrics for evaluating online courses. In particular, we define the Value Score (VS), the Content Efficiency Ratio (CER), and the Advanced Course Score (ACS). These metrics are designed to capture various dimensions of course quality including rating, popularity, affordability, content depth, and recency. We provide detailed derivations and explanations for the formulas, discuss limitations, and present an example comparing two courses.
            </p>
          </section>
          
          <section className="section">
            <h2>Introduction</h2>
            <p style = {{fontSize:"22px", paddingBottom: "10px"}}>
              In the burgeoning field of online education, stakeholders require robust and multifaceted metrics to evaluate course quality. In this paper, we propose three metrics for course evaluation:
            </p>
            <ol>
              <li><strong>Value Score (VS)</strong></li>
              <li><strong>Content Efficiency Ratio (CER)</strong></li>
              <li><strong>Advanced Course Score (ACS)</strong></li>
            </ol>
            <p>
              These metrics use the following parameters:
            </p>
            <ol>
              <li><strong>R</strong>: Course Rating (on a scale from 0 to 5).</li>
              <li><strong>NR</strong>: Number of ratings (a higher NR indicates that the course rating is more reliable).</li>
              <li><strong>S</strong>: Number of Students enrolled (a higher S indicates greater popularity).</li>
              <li><strong>P</strong>: Course price in USD (lower is better, so P appears in the denominator).</li>
              <li><strong>D</strong>: Course Duration in hours (a longer duration typically implies more content and, hence, more value).</li>
              <li><strong>M</strong>: Months since the last update (courses updated more recently are considered more relevant; thus, a lower M is preferable).</li>
            </ol>
            <p>
              The three proposed metrics are defined as follows:
            </p>
            <div className="formulas">
              <Latex className="formula">
                {`\\[
                \\textbf{Value Score (VS)} = \\frac{R \\times \\log_{10}(S+1) \\times \\log_{10}(NR+1) \\times \\left(\\frac{NR}{S} + 1\\right)}{P}
                \\]`}
              </Latex>
              <br />
              <Latex className="formula">
                {`\\[
                \\textbf{Content Efficiency Ratio (CER)} = \\frac{D}{P}
                \\]`}
              </Latex>
              <br />
              <Latex className="formula">
                {`\\[
                \\textbf{Advanced Course Score (ACS)} = \\frac{R \\times \\log_{10}(NR+1)}{M+1} \\times \\log_{10}(S+1) \\times \\frac{1}{\\log_{10}(P+10)} \\times \\frac{D}{10}
                \\]`}
              </Latex>
            </div>
          </section>
          <section className="section">
            <h2>Thoughts Behind the Formulas</h2>
            <p style = {{fontSize:"24px", paddingBottom: "10px"}}>
                The formulation of these metrics is based on several key considerations:
            </p>
            <ul>
            <li>
                <strong>Quality and Reliability:</strong> The course rating (R) is a direct measure of quality. However, its reliability increases with the number of ratings (NR). To balance this, we include 
                &nbsp;<Latex  className="formula">{`\\(\\log_{10}(NR+1)\\)`}</Latex> &nbsp;
                to capture the effect of additional ratings while mitigating extreme values.
            </li>
            <li>
                <strong>Popularity:</strong> Student enrollment (S) serves as a measure of popularity. Given that (S) can span several orders of magnitude, we use 
                &nbsp;<Latex  className="formula">{`\\(\\log_{10}(S+1)\\)`}</Latex>&nbsp;
                to compress the scale and ensure that differences at the lower end are still meaningful.
            </li>
            <li>
                <strong>Engagement:</strong> By incorporating the term &nbsp;
                <Latex  className="formula">{`\\(\\left(\\frac{NR}{S} + 1\\right)\\)`}</Latex>&nbsp;
                in the Value Score, we penalize courses that have many students but few ratings, thereby rewarding courses where a larger fraction of students engage by leaving ratings.
            </li>
            <li>
                <strong>Affordability:</strong> Both (VS) and (CER) include price (P) in the denominator to reward lower-priced courses.
            </li>
            <li>
                <strong>Content Depth:</strong> The duration (D) is used to represent the volume of content, with a longer duration suggesting a more comprehensive course.
            </li>
            <li>
                <strong>Recency:</strong> In the ACS, dividing by (M+1) penalizes courses that have not been updated recently, thus favoring courses with current content.
            </li>
            </ul>
        </section>
      
        <section className="section">
            <h2>Detailed Explanation and Breakdown of the Formulas</h2>
            <h3 style={{fontSize:"22px"}}>Value Score (VS):</h3>
    
            <p style={{paddingBottom: "15px"}}>
            The Value Score is given by:
            </p>
            &emsp;&emsp;<Latex className="formula">
            {`\\[
            \\text{VS} = \\frac{R \\times \\log_{10}(S+1) \\times \\log_{10}(NR+1) \\times \\left(\\frac{NR}{S} + 1\\right)}{P}.
            \\]`}
            </Latex>
            <p style={{paddingBottom: "7px", paddingTop: "10px"}}>
            <strong>Explanation:</strong>
            </p>
            <ul>
            <li>R is the course rating, a direct indicator of quality.</li>
            <li> <Latex  className="formula">
            {`\\[\\log_{10}(S+1)\\]`}
            </Latex> &nbsp;transforms the student count to a manageable scale.</li>
            <li><Latex  className="formula">
            {`\\[\\log_{10}(NR+1) \\]`} 
            </Latex>&nbsp; does the same for the number of ratings, emphasizing reliability.</li>
            <li>The factor &nbsp;
                <Latex  className="formula">{`\\(\\left(\\frac{NR}{S} + 1\\right)\\)`}</Latex>&nbsp; 
                ensures that courses with low engagement (i.e., a low proportion of ratings to students) are penalized.</li>
            <li>Dividing by P ensures that courses with lower prices are rated higher in terms of value.</li>
            </ul>
            
            <br />
            <h3 style={{fontSize:"22px"}}>Content Efficiency Ratio (CER):</h3>
            <p style={{paddingBottom: "15px"}}>
            The Content Efficiency Ratio is defined as:
            </p>
            <Latex className="formula">
            {`\\[
            \\text{CER} = \\frac{D}{P}.
            \\]`}
            </Latex>
            <p style={{paddingBottom: "7px", paddingTop: "10px"}}>
            <strong>Explanation:</strong>
            </p>
            <ul>
            <li>D represents the total duration of the course in hours.</li>
            <li>P is the course price in USD.</li>
            <li>CER provides a direct measure of how many hours of content a learner receives per dollar spent.</li>
            </ul>

            <br />
            <h3 style={{fontSize:"22px"}}>Advanced Course Score (ACS):</h3>
            <p style={{paddingBottom: "15px"}}>
            The Advanced Course Score is formulated as:
            </p>
            <Latex  className="formula">
            {`\\[
            \\text{ACS} = \\frac{R \\times \\log_{10}(NR+1)}{M+1} \\times \\log_{10}(S+1) \\times \\frac{1}{\\log_{10}(P+10)} \\times \\frac{D}{10}.
            \\]`}
            </Latex>
            <p style={{paddingBottom: "7px", paddingTop: "10px"}}>
            <strong>Explanation:</strong>
            </p>
            <ul>
            <li>
                The component &nbsp;
                <Latex  className="formula">{`\\(\\frac{R \\times \\log_{10}(NR+1)}{M+1}\\)`}</Latex> &nbsp;
                integrates quality and recency, rewarding courses with high ratings and many reviews while penalizing those that have not been updated recently.
            </li>
            <li><Latex  className="formula">
            {`\\[\\log_{10}(S+1)\\]`}
            </Latex> &nbsp; again captures the popularity of the course.</li>
            <li>
                The term &nbsp;
                <Latex  className="formula">{`\\(\\frac{1}{\\log_{10}(P+10)}\\)`}</Latex> &nbsp;
                moderates the influence of the price. Adding 10 within the logarithm prevents the price factor from becoming extreme for very low-priced courses.
            </li>
            <li> <Latex className="formula">{`\\[\\frac{D}{10} \\]`}</Latex> &nbsp;normalizes the course duration to maintain balance with the other factors.</li>
            </ul>
        </section>
      
        <section className="section">
            <h2>Limitations</h2>
            <p style = {{fontSize:"24px", paddingBottom: "10px"}}>
            Despite the comprehensive nature of these metrics, several limitations exist:
            </p>
            <ul>
            <li>
                <strong>Sensitivity to Data Distribution:</strong> Logarithmic transformations mitigate extreme values; however, courses with extremely low or high parameter values can still disproportionately influence the metrics.
            </li>
            <li>
                <strong>Parameter Interdependency:</strong> Some parameters, such as (NR) and (S), might be interdependent. The simple multiplicative or additive structure may not fully capture the complexity of these relationships.
            </li>
            <li>
                <strong>Arbitrary Weighting:</strong> The current formulations assume equal importance (implicitly) of the multiplicative components. In practice, we might wish to assign different weights to quality, engagement, content, or recency.
            </li>
            <li>
                <strong>Data Quality and Availability:</strong> These metrics are highly dependent on the availability and precision of the underlying data. Missing or inconsistent data can lead to misleading scores.
            </li>
            <li>
                <strong>Static Nature:</strong> The formulas do not adjust dynamically based on changing trends or feedback, which may require periodic re-calibration.
            </li>
            </ul>
        </section>
      
        <section className="section">
            <h2>Example</h2>
            <p>
            To illustrate the application of these metrics, consider the following example comparing two courses:
            </p>
            <table style={{ borderCollapse: "collapse", width: "100%", textAlign:"center" }} border="1">
            <thead>
                <tr>
                <th>Course</th>
                <th>R</th>
                <th>NR</th>
                <th>S</th>
                <th>P (USD)</th>
                <th>D (hours)</th>
                <th>M</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                <td>Course A</td>
                <td>4.7</td>
                <td>424720</td>
                <td>1415860</td>
                <td>5.75</td>
                <td>61.733</td>
                <td>1</td>
                </tr>
                <tr>
                <td>Course B</td>
                <td>4.9</td>
                <td>6120</td>
                <td>24357</td>
                <td>5.80</td>
                <td>67.55</td>
                <td>0</td>
                </tr>
            </tbody>
            </table>
            <br />
            <p>
            Using these values, the metrics are computed as follows:
            </p>
            <br />
            <p style={{paddingBottom: "15px"}}>
            <strong>Value Score (VS):</strong>
            </p>
            &emsp;&emsp;<Latex  className="formula">
            {`\\[
            \\text{VS} = \\frac{R \\times \\log_{10}(S+1) \\times \\log_{10}(NR+1) \\times \\left(\\frac{NR}{S} + 1\\right)}{P}.
            \\]`}
            </Latex>
            <p style={{paddingBottom: "15px"}}>
            <br />
            <strong>Content Efficiency Ratio (CER):</strong>
            </p>
            &emsp;&emsp;<Latex  className="formula">
            {`\\[
            \\text{CER} = \\frac{D}{P}.
            \\]`}
            </Latex>
            <p style={{paddingBottom: "15px"}}>
            <br />
            <strong style={{paddingBottom: "15px"}}>Advanced Course Score (ACS):</strong>
            </p>
            &emsp;&emsp;<Latex  className="formula">
            {`\\[
            \\text{ACS} = \\frac{R \\times \\log_{10}(NR+1)}{M+1} \\times \\log_{10}(S+1) \\times \\frac{1}{\\log_{10}(P+10)} \\times \\frac{D}{10}.
            \\]`}
            </Latex>
            
            <p>
            <br />
                The resulting scores can be used to rank and compare the courses.
            </p>
        </section>
      
        <section className='section' style = {{paddingBottom:"90px"}}>
            <h2>Conclusion</h2>
            <p>
            This paper presents a set of comprehensive metrics for course evaluation. The Value Score (VS) integrates course quality, popularity, and engagement with price, penalizing courses with low engagement relative to their student base. The Content Efficiency Ratio (CER) provides a direct measure of content delivered per unit cost, and the Advanced Course Score (ACS) offers a nuanced composite score that also accounts for recency. Although each metric has limitations, together they provide a multifaceted view of course quality that can assist stakeholders in making informed decisions.
            </p>
        </section>
        
        </div>
        <Footer />
      </div>
      
    </>
  );
};

export default Procedures;
