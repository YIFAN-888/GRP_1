import cv2
import picture as pic
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX  #フォントを設置
size = 0.5  # フォントのサイズを設定します
width, height = 300, 300  # ウィンドウのサイズを設定します
x0, y0 = 300, 100  # ピック位置を設定する
cnt = 1
cap = cv2.VideoCapture(0)  # カメラの電源をオン

if __name__ == "__main__":
    while (1):
        flag, frame = cap.read()  # カメラの内容を読む
        frame = cv2.flip(frame, 2)
        roi, res, ret, fourier_result, efd_result = pic.binaryMask(frame, x0, y0, width, height)  # ジェスチャのブロック図を取り、それを処理します
        #cv2.imshow("roi", roi)  # ジェスチャーブロック図を表示する
        cv2.imshow("res", res)
        #cv2.imshow("ret", ret)
        key = cv2.waitKey(1) & 0xFF  # キーを押して判断し、特定の調整を行います
        #'j''l''u''j'を押して、選択ボックスをそれぞれ左、右、上、下に移動します
        # [Ｑ]quit
        if key == ord('i'):
            y0 += 5
        elif key == ord('k'):
            y0 -= 5
        elif key == ord('l'):
            x0 += 5
        elif key == ord('j'):
            x0 -= 5
        elif key == ord('q'):
            break
        elif key == ord('s'):
            path = './' + 'test_image' + '/'
            name = str(cnt)
            cv2.imwrite(path + 'roi_sun.png', roi)
            cnt += 1
            cv2.imwrite(path + name+'.png',res)
        elif key == ord('p'):
            descirptor_in_use = abs(fourier_result)
            fd_test = np.zeros((1, 31))
            temp = descirptor_in_use[1]
        cv2.imshow('frame', frame)  # カメラの内容
    cap.release()
    cv2.destroyAllWindows()  # すべてのウィンドウを閉じる