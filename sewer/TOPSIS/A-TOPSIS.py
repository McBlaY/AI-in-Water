# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 13:19:36 2021

@author: vanln
"""

from tkinter import Tk, TOP, CENTER, LEFT, RIGHT, END
from tkinter import Frame, Entry, Button, Label, LabelFrame
from tkinter import filedialog, messagebox
import os
import numpy as np
import pandas as pd


def TaoForm(dl, w, h):
    # get screen width and height
    ws = dl.winfo_screenwidth()  # width of the screen
    hs = dl.winfo_screenheight()  # height of the screen
    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    dl.geometry("%dx%d+%d+%d" % (w, h, x, y))


dialog = Tk()
dialog.title("A-TOPSIS")
TaoForm(dialog, 500, 200)
frame0 = Frame(dialog)
frame0.pack(fill="both", side=TOP, padx=5, pady=5)
frame1 = Frame(dialog)
frame1.pack(fill="both", padx=5, pady=5)
frame10 = Frame(dialog)
frame10.pack(fill="both", padx=5, pady=5)
mau = Entry(frame1, justify=CENTER)
mau.pack(fill="both", expand="yes", side=LEFT, padx=5, pady=5)
mau.delete(0, END)
mau.insert(0, "R2, MAE, MAPE, RMSE, RAE, RRSE")
sl_thongke = Entry()


def thongke_file():
    file_sl = filedialog.askopenfilenames(
        title="Open Statistical File(s)", filetype=(("csv files", "*.csv"),)
    )
    if len(file_sl) > 0:
        chuoi = ""
        for i in range(len(file_sl)):
            chuoi += file_sl[i] + "}"
        sl_thongke.delete(0, END)
        sl_thongke.insert(0, chuoi)
    else:
        messagebox.showerror("Error", "Input Statistical File(s)")


btn_tk_file = Button(
    frame1,
    text="Open File(s)",
    font="Tahoma 9 bold",
    height=1,
    justify=CENTER,
    command=thongke_file,
)
btn_tk_file.pack(fill="both", side=LEFT, padx=5, pady=5)


def thongke():
    if sl_thongke.get() != "":
        file_sl = sl_thongke.get()
        file_sl = list(file_sl.split("}"))
        folder = os.path.dirname(file_sl[0])
        if len(file_sl) - 1 == 1:
            t = os.path.basename(file_sl[0]).split(".")[0]
        else:
            t = "overview"
        kq = open(folder + "/modified_" + t + ".csv", "w")
        kq1 = open(folder + "/TOPSIS_" + t + ".txt", "w")
        gt = list(str(mau.get()).split(","))
        for i in range(len(file_sl) - 1):
            sl_file = str(file_sl[i]).strip()
            name = os.path.basename(sl_file).split(".")[0]
            kq.write("- ," + name + ",:" + "\n")
            kq1.write("- " + name + ":" + "\n" + "\n")
            data = pd.DataFrame(pd.read_csv(sl_file))
            ten = data.columns.values
            tb = data.mean(axis=0)
            std = data.std(axis=0)
            dem = int(len(ten) / len(gt))
            t = 0
            # Chuan hoa cho A-TOPSIS
            kq1.write(20 * " ")
            for j in range(len(gt)):
                bien = str(gt[j]).strip()
                b = "Mean_" + bien
                kq1.write(b.center(20) + " ")
            for j in range(len(gt)):
                bien = str(gt[j]).strip()
                b = "Std_" + bien
                kq1.write(b.center(20) + " ")
            kq1.write("\n")
            for j in range(dem):
                kt = "_" + gt[0]
                kt1 = str(ten[t]).replace(kt, "")
                kq1.write(kt1.center(19))
                for k in range(len(gt)):
                    t1 = round(float(tb.iloc[t + k]), 6)
                    kq1.write(str(t1).center(14))
                for k in range(len(gt)):
                    t1 = round(float(std.iloc[t + k]), 6)
                    kq1.write(str(t1).center(14))
                t += k + 1
                kq1.write("\n")
            kq1.write("\n" + "\n")
            # Chuan hoa
            for j in range(len(gt)):
                bien = str(gt[j]).strip()
                kq.write("  + " + bien + ":" + "\n")
                f = open(sl_file, "r")
                dodaifile = len(f.read().splitlines())
                sl = open(sl_file, "r")
                dong = sl.readline().strip()
                socot, cot = [], []
                for k in range(0, len(dong.split(","))):
                    socot += [dong.split(",")[k].strip()]
                for k in range(len(socot)):
                    if bien in socot[k]:
                        cot += [socot[k]]
                kq.write(",".join([str(item) for item in cot]) + "\n")
                luu_gt = []
                for k in range(0, dodaifile - 1):
                    dong = sl.readline().strip()
                    luu = []
                    for a in range(0, len(socot)):
                        if bien in socot[a]:
                            luu += [dong.split(",")[a]]
                            luu_gt += [luu]
                    kq.write(",".join([str(item) for item in luu]) + "\n")
                sl.close()
            kq.write("\n" + "\n")
        kq.close()
        kq1.close()
        messagebox.showinfo(title="Phd Dissertation/Thesis", message="Calculation Complete.")
    else:
        messagebox.showerror("Error", "Input Modified File(s)")


btn_tk = Button(
    frame1, text="Modify", font="Tahoma 9 bold", height=1, justify=CENTER, command=thongke
)
btn_tk.pack(fill="both", side=RIGHT, padx=5, pady=5)

frame_TOPSIS = LabelFrame(frame10, text="Algorithm Selection - TOPSIS", font="Tahoma 9 bold")
frame_TOPSIS.pack(fill="both", padx=5, pady=5)
label_TOPSIS1 = Label(frame_TOPSIS, text="Criteria")
label_TOPSIS1.pack(fill="both", side=LEFT, padx=5, pady=5)
criteria_TOPSIS = Entry(frame_TOPSIS, justify=CENTER)
criteria_TOPSIS.pack(fill="both", side=LEFT, expand="yes", padx=5, pady=5)
criteria_TOPSIS.delete(0, END)
criteria_TOPSIS.insert(0, "1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1")


def topsis():
    file_sl = filedialog.askopenfilename(
        title="Open file to calculate A-TOPSIS algorithm", filetype=(("txt files", "*.txt"),)
    )
    if len(file_sl) > 0:
        file_sl = file_sl.replace("/", "\\")
        f = open(file_sl, "r")
        dodai = len(f.read().splitlines())
        folder = os.path.dirname(file_sl)
        fileopen = open(file_sl, "r")
        t = os.path.basename(file_sl).split(".")[0]
        kq = open(folder + "/Ranking_" + t + ".txt", "w")
        chuoi, dem = [], 0
        gt = list(str(criteria_TOPSIS.get()).split(","))
        for i in range(0, dodai):
            dong = fileopen.readline().strip()
            chuoi.append(dong)
            if (dong.count(":") == 1 and dem == 1) or (i == dodai - 1):
                kq.write(chuoi[:-1][0] + "\n" + "\n")
                data = []
                for j in range(1, len(chuoi[:-1])):
                    if len(chuoi[:-1][j].strip()) > 1:
                        data.append(chuoi[:-1][j].strip())
                column = len(data[0].split())
                bang, name = [], []
                for j in range(1, len(data)):
                    bang.append(data[j].strip())
                for j in range(len(bang)):
                    name.append(bang[j].split()[0].strip())
                if column == len(gt):
                    matrix, a_positive, a_negative = [], [], []
                    for n in range(len(bang)):
                        matrix.append([])
                        kt = list(bang[n].split())
                        for m in range(1, len(kt)):
                            if len(kt[m]) > 0:
                                matrix[n].append(float(kt[m].strip()))
                    matrix = np.array(matrix)
                    tong_cot = np.sum(matrix, axis=0)
                    for n in range(matrix.shape[0]):
                        for m in range(matrix.shape[1]):
                            matrix[n][m] = matrix[n][m] / tong_cot[m]
                            if matrix[n][m] < 0:
                                matrix[n][m] = pow(10, -20)
                    for n in range(len(gt)):
                        if gt[n].strip() == "1":
                            a_positive.append(np.amax(matrix, axis=0)[n])
                            a_negative.append(np.amin(matrix, axis=0)[n])
                        elif gt[n].strip() == "-1":
                            a_positive.append(np.amin(matrix, axis=0)[n])
                            a_negative.append(np.amax(matrix, axis=0)[n])
                        else:
                            messagebox.showerror(
                                "Criteria Error",
                                str(gt[n])
                                + "\n"
                                + "Please re-check Criteria."
                                + "\n"
                                + "1 for maximum, -1 for mininmum.",
                            )
                    a_positive, a_negative = np.array(a_positive), np.array(a_negative)
                    matrix_p = matrix * np.log(matrix)
                    tong_cot_p = np.sum(matrix_p, axis=0)
                    tong_cot_p = 1 + (1 / (np.log(matrix_p.shape[0]))) * tong_cot_p
                    tong_hang_p, w = [], []
                    for n in range(2):
                        bien = np.sum(tong_cot_p[n : (n + int(len(gt) / 2))])
                        tong_hang_p.append(bien)
                    tong_hang_p = np.array(tong_hang_p)
                    t, tt = int(len(gt) / 2), 0
                    for n in range(2):
                        bien = tong_cot_p[n + tt : n + t + tt] / tong_hang_p[n]
                        tt = t - 1
                        w.append(bien)
                    w, ww = np.array(w), []
                    d_positive, d_negative = (
                        pow((a_positive - matrix), 2),
                        pow((a_negative - matrix), 2),
                    )
                    for n in range(w.shape[0]):
                        for m in range(w.shape[1]):
                            ww.append(w[n][m])
                    for n in range(matrix.shape[0]):
                        for m in range(matrix.shape[1]):
                            d_positive[n][m] = d_positive[n][m] * ww[m]
                            d_negative[n][m] = d_negative[n][m] * ww[m]
                    dd_positive, dd_negative, t, tt = [], [], int(len(gt) / 2), 0
                    for n in range(2):
                        bien1 = np.sum(d_positive[:, n + tt : n + t + tt], axis=1)
                        dd_positive.append(bien1)
                        bien2 = np.sum(d_negative[:, n + tt : n + t + tt], axis=1)
                        dd_negative.append(bien2)
                        tt = t - 1
                    dd_positive, dd_negative = (
                        np.sqrt(np.array(dd_positive)),
                        np.sqrt(np.array(dd_negative)),
                    )
                    rank = []
                    for n in range(dd_positive.shape[0]):
                        bien = dd_negative[n] / (dd_negative[n] + dd_positive[n])
                        rank.append(bien.tolist())
                    rank = np.array(rank)
                    rank = np.nan_to_num(rank, nan=0)
                    # Tinh final A-TOPSIS
                    matrix_final = np.transpose(rank)
                    tong_cot_final = np.sum(matrix_final, axis=0)
                    for n in range(matrix_final.shape[0]):
                        for m in range(matrix_final.shape[1]):
                            matrix_final[n][m] = matrix_final[n][m] / tong_cot_final[m]
                            if matrix_final[n][m] <= 0:
                                matrix_final[n][m] = pow(10, -20)
                    a_positive, a_negative = [], []
                    for n in range(2):
                        a_positive.append(np.amax(matrix_final, axis=0)[n])
                        a_negative.append(np.amin(matrix_final, axis=0)[n])
                    a_positive, a_negative = np.array(a_positive), np.array(a_negative)
                    matrix_p_final = matrix_final * np.log(matrix_final)
                    tong_cot_p_final = np.sum(matrix_p_final, axis=0)
                    tong_cot_p_final = (
                        1 + (1 / (np.log(matrix_p_final.shape[0]))) * tong_cot_p_final
                    )
                    tong_hang_p_final = np.sum(tong_cot_p_final, axis=0)
                    w_final = np.array(tong_cot_p_final / tong_hang_p_final)
                    dd_positive_final = pow((a_positive - matrix_final), 2) * w_final
                    dd_negative_final = pow((a_negative - matrix_final), 2) * w_final
                    bien1 = np.sum(dd_positive_final, axis=1)
                    bien2 = np.sum(dd_negative_final, axis=1)
                    rank_final = np.sqrt(bien2) / (np.sqrt(bien1) + np.sqrt(bien2))
                    df = pd.DataFrame()
                    df["rank"], df["name"], df["ratio1"], df["ratio2"] = (
                        rank_final,
                        name,
                        rank[0],
                        rank[1],
                    )
                    # Sap xep dataFrame theo thu tu giam dan
                    df_sort = df.sort_values(by=["rank"], ascending=False)
                    kq.write(
                        "Architecture".center(15)
                        + "Ratio_Mean".center(12)
                        + "Ratio_Std".center(12)
                        + "Ratio_Total".center(12)
                        + "Ranking".center(9)
                        + "\n"
                    )
                    name, ratio1 = (
                        df_sort["name"].values.tolist(),
                        df_sort["ratio1"].values.tolist(),
                    )
                    ratio2, rank = (
                        df_sort["ratio2"].values.tolist(),
                        df_sort["rank"].values.tolist(),
                    )
                    for n in range(len(name)):
                        kq.write(
                            str(name[n]).center(15)
                            + str(round(ratio1[n], 4)).center(12)
                            + str(round(ratio2[n], 4)).center(12)
                            + str(round(rank[n], 4)).center(12)
                        )
                        if str(rank[n]) == "nan":
                            nn = "---"
                        else:
                            nn = n + 1
                        kq.write(str(nn).center(9) + "\n")
                    kq.write("\n" + "\n")
                else:
                    messagebox.showerror(
                        "Inconsistent Data",
                        "Please re-check Criteria."
                        + "\n"
                        + "Number of Criteria = Number of columns - 1.",
                    )
                chuoi.clear()
                chuoi.append(dong)
            dem = 1
        fileopen.close()
        kq.close()
        messagebox.showinfo(title="Phd Dissertation/Thesis", message="Calculation Complete.")
    else:
        messagebox.showerror("Error", "Input File to calculate.")


btn_TOPSIS_open = Button(
    frame_TOPSIS,
    text="Run A-TOPSIS",
    font="Tahoma 9 bold",
    fg="white",
    bg="blue",
    height=1,
    justify=CENTER,
    command=topsis,
)
btn_TOPSIS_open.pack(fill="both", side=RIGHT, padx=5, pady=5)
dialog.mainloop()
