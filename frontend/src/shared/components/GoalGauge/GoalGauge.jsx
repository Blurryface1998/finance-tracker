import "./GoalGauge.scss";

const GAUGE_PATH =
  "M121.6 64C125.135 64 128.033 61.1276 127.68 57.6106C127.057 51.3979 125.527 45.2981 123.128 39.5083C119.912 31.7434 115.198 24.6881 109.255 18.7452C103.312 12.8022 96.2566 8.08801 88.4917 4.87171C80.7269 1.65541 72.4046 -3.67377e-07 64 0C55.5954 3.67377e-07 47.2731 1.65541 39.5083 4.87171C31.7434 8.08801 24.6881 12.8022 18.7452 18.7452C12.8022 24.6881 8.08801 31.7434 4.87171 39.5083C2.47348 45.2981 0.943094 51.3979 0.319734 57.6106C-0.0331434 61.1276 2.86538 64 6.4 64C9.93462 64 12.7588 61.1237 13.1995 57.6166C13.7688 53.0863 14.9427 48.6427 16.6974 44.4066C19.2704 38.1947 23.0418 32.5505 27.7961 27.7961C32.5505 23.0418 38.1947 20.2704 44.4066 16.6974C50.6185 14.1243 57.2763 12.8 64 12.8C70.7237 12.8 77.3815 14.1243 83.5934 16.6974C89.8053 19.2704 95.4495 23.0418 100.204 27.7961C104.958 32.5505 108.73 38.1947 111.303 44.4066C113.057 48.6427 114.231 53.0862 114.801 57.6166C115.241 61.1236 118.065 64 121.6 64Z";

const PROGRESS_PATH =
  "M104.729 23.2707C107.229 20.7713 107.247 16.6905 104.511 14.4532C96.4186 7.83682 86.8012 3.28163 76.4858 1.22977C64.071 -1.23968 51.2027 0.0277319 39.5083 4.87174C27.8138 9.71575 17.8183 17.9188 10.7859 28.4435C4.94273 37.1885 1.36322 47.21 0.319708 57.6105C-0.0331616 61.1274 2.86538 64 6.4 64C9.93462 64 12.7588 61.1236 13.1995 57.6165C14.1877 49.7521 16.9928 42.1937 21.4288 35.5548C27.0547 27.135 35.051 20.5726 44.4066 16.6974C53.7622 12.8222 64.0568 11.8083 73.9886 13.7838C81.8196 15.3415 89.1478 18.7026 95.4076 23.5648C98.1991 25.733 102.23 25.77 104.729 23.2707Z";

/*
 * Needle shape from the Figma meter.
 *
 * This is the upper/needle portion of the exported meter.
 * The circular part is intentionally NOT included here.
 */
const NEEDLE_PATH =
  "M69.7232 60.1883L93.9985 32.0009L66.3309 56.4689C65.6147 56.1669 64.8276 56 64.0015 56";

function GoalGauge({ current, goal }) {
  const safeGoal = Number(goal) > 0 ? Number(goal) : 1;

  const progress = Math.min(Math.max(Number(current) / safeGoal, 0), 1);

  /*
   * Meter behaves like a clock hand.
   *
   * 0%   = left
   * 50%  = top
   * 100% = right
   *
   * The Figma polygon's original angle is approximately -44.92deg.
   */
  const needleRotation = -134.92 + progress * 180;

  return (
    <div className="graph">
      <div className="goal-gauge">
        <svg
          className="goal-gauge__svg"
          viewBox="0 0 128 68"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          aria-label="Goal progress gauge"
        >
          {/* Fixed background graph */}
          <path className="goal-gauge__track" d={GAUGE_PATH} />

          {/* Existing progress graph */}
          <path className="goal-gauge__progress" d={PROGRESS_PATH} />

          {/* Meter needle */}
          <g
            className="goal-gauge__needle-wrapper"
            transform={`rotate(${needleRotation} 64 62)`}
          >
            <path className="goal-gauge__needle" d={NEEDLE_PATH} />
          </g>

          {/* Fixed meter center / Ellipse 25 */}
          <circle className="goal-gauge__pivot" cx="64" cy="62" r="6" />
        </svg>
      </div>
      <div className="goal-gauge__range">
        <p>$0</p>
        <p>{current}K</p>
        <p>${goal}</p>
      </div>
    </div>
  );
}

export default GoalGauge;
