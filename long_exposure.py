#import line : 필수 페키지
import argparse
import imutils
import cv2

#인수 구문 분석(argparse)
argp = argparse.ArgumentParser()

argp.add_argument("-v", "--video", required=True,
	help="Input 비디오의 경로")

argp.add_argument("-o", "--output", required=True,
	help="장노출 결과물의 Output 경로'")

args = vars(argp.parse_args())


#RGB 체널 불러오기 & 프레임 갯수 읽기
(Rg, Gg ,Bg) = (None, None, None)
total = 0

#비디오 불러들이기
print("------open-------")
stream = cv2.VideoCapture(args["video"])
print("-------take--------")

#비디오 스트림의 프레임에 loop over
while True:
    #grab the frame the file stream
    (grabbed, frame) = stream.read()

    #프레임 인식 불가시 종료
    if not grabbed:
        break
    #그게 아니면 프레임을 해당체널로 분리
    (B, G, R) = cv2.split(frame.astype("float"))

    #프레임간 평균이 없으면 초기화
    if Rg is None:
        Rg = R
        Bg = B
        Gg = G
    #그렇지 않으면 프레임 기록과 현재 프레임 간의 가중 평균을 계산
    else:
        Rg = ((total * Rg) + (1 * R)) / (total + 1.0)
        Gg = ((total * Gg) + (1 * G)) / (total + 1.0)
        Bg = ((total * Bg) + (1 * B)) / (total + 1.0)

        total += 1

#RGB 평균을 병합하고 출력 이미지를 디스크에 기록
avg = cv2.merge([Bg, Gg, Rg]).astype("uint8")
cv2.imwrite(args["output"], avg)

stream.release()



