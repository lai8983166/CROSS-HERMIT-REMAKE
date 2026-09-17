
undefined4 __fastcall FUN__text__0053ecc8(int param_1)

{
  char *pcVar1;
  char *pcVar2;
  undefined4 uVar3;
  uint uVar4;
  int iVar5;
  int iVar6;
  uint uVar7;
  bool bVar8;
  int iStack_40;
  char local_30 [16];
  uint local_20;
  char *local_1c;
  char *local_18;
  char *local_14;
  char *local_10;
  int local_c;
  uint local_8;
  
  local_c = param_1;
  local_8 = 0;
  local_10 = (char *)0x0;
  local_18 = (char *)0x0;
  local_14 = (char *)0x0;
  local_1c = (char *)0x0;
  pcVar1 = (char *)(param_1 + 200);
  for (pcVar2 = pcVar1; (*pcVar2 != '\0' && (*pcVar2 != '_')); pcVar2 = pcVar2 + 1) {
  }
  if (*pcVar2 != '\0') {
    local_18 = pcVar2 + 1;
    local_10 = local_18;
    for (; (*local_18 != '\0' && (*local_18 != '_')); local_18 = local_18 + 1) {
    }
    if (*local_18 != '\0') {
      local_1c = local_18 + 1;
      local_14 = local_1c;
      for (; *local_1c != '\0'; local_1c = local_1c + 1) {
      }
    }
  }
  uVar7 = (int)pcVar2 - (int)pcVar1;
  if (0xf < uVar7) {
    return 0x109;
  }
  pcVar2 = local_30;
  for (uVar4 = uVar7 >> 2; uVar4 != 0; uVar4 = uVar4 - 1) {
    *(undefined4 *)pcVar2 = *(undefined4 *)pcVar1;
    pcVar1 = pcVar1 + 4;
    pcVar2 = pcVar2 + 4;
  }
  for (uVar4 = uVar7 & 3; uVar4 != 0; uVar4 = uVar4 - 1) {
    *pcVar2 = *pcVar1;
    pcVar1 = pcVar1 + 1;
    pcVar2 = pcVar2 + 1;
  }
  local_30[uVar7] = '\0';
  iStack_40 = 4;
  bVar8 = true;
  iVar5 = iStack_40;
  pcVar2 = local_30;
  pcVar1 = "nop";
  do {
    if (iVar5 == 0) break;
    iVar5 = iVar5 + -1;
    bVar8 = *pcVar2 == *pcVar1;
    pcVar2 = pcVar2 + 1;
    pcVar1 = pcVar1 + 1;
  } while (bVar8);
  if (bVar8) {
    iStack_40 = 0;
LAB__text__0053f0bd:
    uVar3 = 0x104;
  }
  else {
    bVar8 = true;
    iVar5 = iStack_40;
    pcVar2 = local_30;
    pcVar1 = "mov";
    do {
      if (iVar5 == 0) break;
      iVar5 = iVar5 + -1;
      bVar8 = *pcVar2 == *pcVar1;
      pcVar2 = pcVar2 + 1;
      pcVar1 = pcVar1 + 1;
    } while (bVar8);
    if (bVar8) {
      iStack_40 = 1;
      goto LAB__text__0053f2af;
    }
    bVar8 = true;
    iVar5 = iStack_40;
    pcVar2 = local_30;
    pcVar1 = "add";
    do {
      if (iVar5 == 0) break;
      iVar5 = iVar5 + -1;
      bVar8 = *pcVar2 == *pcVar1;
      pcVar2 = pcVar2 + 1;
      pcVar1 = pcVar1 + 1;
    } while (bVar8);
    if (bVar8) {
      iStack_40 = 2;
      iVar5 = iStack_40;
    }
    else {
      bVar8 = true;
      iVar5 = iStack_40;
      pcVar2 = local_30;
      pcVar1 = "sub";
      do {
        if (iVar5 == 0) break;
        iVar5 = iVar5 + -1;
        bVar8 = *pcVar2 == *pcVar1;
        pcVar2 = pcVar2 + 1;
        pcVar1 = pcVar1 + 1;
      } while (bVar8);
      iVar5 = 3;
      if (!bVar8) {
        bVar8 = true;
        iVar5 = iStack_40;
        pcVar2 = local_30;
        pcVar1 = "mad";
        do {
          if (iVar5 == 0) break;
          iVar5 = iVar5 + -1;
          bVar8 = *pcVar2 == *pcVar1;
          pcVar2 = pcVar2 + 1;
          pcVar1 = pcVar1 + 1;
        } while (bVar8);
        if (bVar8) goto LAB__text__0053ee61;
        bVar8 = true;
        iVar5 = iStack_40;
        pcVar2 = local_30;
        pcVar1 = "mul";
        do {
          if (iVar5 == 0) break;
          iVar5 = iVar5 + -1;
          bVar8 = *pcVar2 == *pcVar1;
          pcVar2 = pcVar2 + 1;
          pcVar1 = pcVar1 + 1;
        } while (bVar8);
        if (bVar8) {
          iStack_40 = 5;
          iVar5 = iStack_40;
        }
        else {
          bVar8 = true;
          iVar5 = iStack_40;
          pcVar2 = local_30;
          pcVar1 = "dp3";
          do {
            if (iVar5 == 0) break;
            iVar5 = iVar5 + -1;
            bVar8 = *pcVar2 == *pcVar1;
            pcVar2 = pcVar2 + 1;
            pcVar1 = pcVar1 + 1;
          } while (bVar8);
          if (bVar8) {
            iStack_40 = 8;
            iVar5 = iStack_40;
          }
          else {
            bVar8 = true;
            iVar5 = iStack_40;
            pcVar2 = local_30;
            pcVar1 = "dp4";
            do {
              if (iVar5 == 0) break;
              iVar5 = iVar5 + -1;
              bVar8 = *pcVar2 == *pcVar1;
              pcVar2 = pcVar2 + 1;
              pcVar1 = pcVar1 + 1;
            } while (bVar8);
            if (!bVar8) {
              bVar8 = true;
              iVar5 = iStack_40;
              pcVar2 = local_30;
              pcVar1 = "frc";
              do {
                if (iVar5 == 0) break;
                iVar5 = iVar5 + -1;
                bVar8 = *pcVar2 == *pcVar1;
                pcVar2 = pcVar2 + 1;
                pcVar1 = pcVar1 + 1;
              } while (bVar8);
              if (bVar8) {
                iStack_40 = 0x13;
              }
              else {
                if (*(int *)(local_c + 0xac) != 0) {
                  bVar8 = true;
                  iVar5 = iStack_40;
                  pcVar2 = local_30;
                  pcVar1 = "lrp";
                  do {
                    if (iVar5 == 0) break;
                    iVar5 = iVar5 + -1;
                    bVar8 = *pcVar2 == *pcVar1;
                    pcVar2 = pcVar2 + 1;
                    pcVar1 = pcVar1 + 1;
                  } while (bVar8);
                  if (bVar8) {
                    iStack_40 = 0x12;
                  }
                  else {
                    bVar8 = true;
                    iVar5 = iStack_40;
                    pcVar2 = local_30;
                    pcVar1 = "cnd";
                    do {
                      if (iVar5 == 0) break;
                      iVar5 = iVar5 + -1;
                      bVar8 = *pcVar2 == *pcVar1;
                      pcVar2 = pcVar2 + 1;
                      pcVar1 = pcVar1 + 1;
                    } while (bVar8);
                    if (bVar8) {
                      iStack_40 = 0x50;
                    }
                    else {
                      bVar8 = true;
                      iVar5 = iStack_40;
                      pcVar2 = local_30;
                      pcVar1 = "cmp";
                      do {
                        if (iVar5 == 0) break;
                        iVar5 = iVar5 + -1;
                        bVar8 = *pcVar2 == *pcVar1;
                        pcVar2 = pcVar2 + 1;
                        pcVar1 = pcVar1 + 1;
                      } while (bVar8);
                      if (!bVar8) {
                        if (*(uint *)(local_c + 0xb4) < 0xffff0104) {
                          iVar5 = 9;
                          bVar8 = true;
                          pcVar2 = local_30;
                          pcVar1 = "texcoord";
                          do {
                            if (iVar5 == 0) break;
                            iVar5 = iVar5 + -1;
                            bVar8 = *pcVar2 == *pcVar1;
                            pcVar2 = pcVar2 + 1;
                            pcVar1 = pcVar1 + 1;
                          } while (bVar8);
                          if (bVar8) {
                            iStack_40 = 0x40;
                          }
                          else {
                            iVar5 = 8;
                            bVar8 = true;
                            pcVar2 = local_30;
                            pcVar1 = "texkill";
                            do {
                              if (iVar5 == 0) break;
                              iVar5 = iVar5 + -1;
                              bVar8 = *pcVar2 == *pcVar1;
                              pcVar2 = pcVar2 + 1;
                              pcVar1 = pcVar1 + 1;
                            } while (bVar8);
                            if (bVar8) {
LAB__text__0053ef20:
                              iStack_40 = 0x41;
                            }
                            else {
                              bVar8 = true;
                              iVar5 = iStack_40;
                              pcVar2 = local_30;
                              pcVar1 = "tex";
                              do {
                                if (iVar5 == 0) break;
                                iVar5 = iVar5 + -1;
                                bVar8 = *pcVar2 == *pcVar1;
                                pcVar2 = pcVar2 + 1;
                                pcVar1 = pcVar1 + 1;
                              } while (bVar8);
                              if (!bVar8) {
                                iVar5 = 7;
                                bVar8 = true;
                                pcVar2 = local_30;
                                pcVar1 = "texbem";
                                do {
                                  if (iVar5 == 0) break;
                                  iVar5 = iVar5 + -1;
                                  bVar8 = *pcVar2 == *pcVar1;
                                  pcVar2 = pcVar2 + 1;
                                  pcVar1 = pcVar1 + 1;
                                } while (bVar8);
                                if (bVar8) {
                                  iStack_40 = 0x43;
                                }
                                else {
                                  iVar5 = 8;
                                  bVar8 = true;
                                  pcVar2 = local_30;
                                  pcVar1 = "texbeml";
                                  do {
                                    if (iVar5 == 0) break;
                                    iVar5 = iVar5 + -1;
                                    bVar8 = *pcVar2 == *pcVar1;
                                    pcVar2 = pcVar2 + 1;
                                    pcVar1 = pcVar1 + 1;
                                  } while (bVar8);
                                  if (bVar8) {
                                    iStack_40 = 0x44;
                                  }
                                  else {
                                    iVar5 = 10;
                                    bVar8 = true;
                                    pcVar2 = local_30;
                                    pcVar1 = "texreg2ar";
                                    do {
                                      if (iVar5 == 0) break;
                                      iVar5 = iVar5 + -1;
                                      bVar8 = *pcVar2 == *pcVar1;
                                      pcVar2 = pcVar2 + 1;
                                      pcVar1 = pcVar1 + 1;
                                    } while (bVar8);
                                    if (bVar8) {
                                      iStack_40 = 0x45;
                                    }
                                    else {
                                      iVar5 = 10;
                                      bVar8 = true;
                                      pcVar2 = local_30;
                                      pcVar1 = "texreg2gb";
                                      do {
                                        if (iVar5 == 0) break;
                                        iVar5 = iVar5 + -1;
                                        bVar8 = *pcVar2 == *pcVar1;
                                        pcVar2 = pcVar2 + 1;
                                        pcVar1 = pcVar1 + 1;
                                      } while (bVar8);
                                      if (bVar8) {
                                        iStack_40 = 0x46;
                                      }
                                      else {
                                        iVar5 = 0xb;
                                        bVar8 = true;
                                        pcVar2 = local_30;
                                        pcVar1 = "texm3x2pad";
                                        do {
                                          if (iVar5 == 0) break;
                                          iVar5 = iVar5 + -1;
                                          bVar8 = *pcVar2 == *pcVar1;
                                          pcVar2 = pcVar2 + 1;
                                          pcVar1 = pcVar1 + 1;
                                        } while (bVar8);
                                        if (bVar8) {
                                          iStack_40 = 0x47;
                                        }
                                        else {
                                          iVar5 = 0xb;
                                          bVar8 = true;
                                          pcVar2 = local_30;
                                          pcVar1 = "texm3x2tex";
                                          do {
                                            if (iVar5 == 0) break;
                                            iVar5 = iVar5 + -1;
                                            bVar8 = *pcVar2 == *pcVar1;
                                            pcVar2 = pcVar2 + 1;
                                            pcVar1 = pcVar1 + 1;
                                          } while (bVar8);
                                          if (bVar8) {
                                            iStack_40 = 0x48;
                                          }
                                          else {
                                            iVar5 = 0xb;
                                            bVar8 = true;
                                            pcVar2 = local_30;
                                            pcVar1 = "texm3x3pad";
                                            do {
                                              if (iVar5 == 0) break;
                                              iVar5 = iVar5 + -1;
                                              bVar8 = *pcVar2 == *pcVar1;
                                              pcVar2 = pcVar2 + 1;
                                              pcVar1 = pcVar1 + 1;
                                            } while (bVar8);
                                            if (bVar8) {
                                              iStack_40 = 0x49;
                                            }
                                            else {
                                              iVar5 = 0xb;
                                              bVar8 = true;
                                              pcVar2 = local_30;
                                              pcVar1 = "texm3x3tex";
                                              do {
                                                if (iVar5 == 0) break;
                                                iVar5 = iVar5 + -1;
                                                bVar8 = *pcVar2 == *pcVar1;
                                                pcVar2 = pcVar2 + 1;
                                                pcVar1 = pcVar1 + 1;
                                              } while (bVar8);
                                              if (bVar8) {
                                                iStack_40 = 0x4a;
                                              }
                                              else {
                                                iVar5 = 0xc;
                                                bVar8 = true;
                                                pcVar2 = local_30;
                                                pcVar1 = "texm3x3spec";
                                                do {
                                                  if (iVar5 == 0) break;
                                                  iVar5 = iVar5 + -1;
                                                  bVar8 = *pcVar2 == *pcVar1;
                                                  pcVar2 = pcVar2 + 1;
                                                  pcVar1 = pcVar1 + 1;
                                                } while (bVar8);
                                                if (bVar8) {
                                                  iStack_40 = 0x4c;
                                                  iVar5 = iStack_40;
                                                  goto LAB__text__0053f292;
                                                }
                                                iVar5 = 0xd;
                                                bVar8 = true;
                                                pcVar2 = local_30;
                                                pcVar1 = "texm3x3vspec";
                                                do {
                                                  if (iVar5 == 0) break;
                                                  iVar5 = iVar5 + -1;
                                                  bVar8 = *pcVar2 == *pcVar1;
                                                  pcVar2 = pcVar2 + 1;
                                                  pcVar1 = pcVar1 + 1;
                                                } while (bVar8);
                                                if (bVar8) {
                                                  iStack_40 = 0x4d;
                                                }
                                                else {
                                                  iVar5 = 0xd;
                                                  bVar8 = true;
                                                  pcVar2 = local_30;
                                                  pcVar1 = "texm3x2depth";
                                                  do {
                                                    if (iVar5 == 0) break;
                                                    iVar5 = iVar5 + -1;
                                                    bVar8 = *pcVar2 == *pcVar1;
                                                    pcVar2 = pcVar2 + 1;
                                                    pcVar1 = pcVar1 + 1;
                                                  } while (bVar8);
                                                  if (bVar8) {
                                                    iStack_40 = 0x54;
                                                  }
                                                  else {
                                                    iVar5 = 7;
                                                    bVar8 = true;
                                                    pcVar2 = local_30;
                                                    pcVar1 = "texdp3";
                                                    do {
                                                      if (iVar5 == 0) break;
                                                      iVar5 = iVar5 + -1;
                                                      bVar8 = *pcVar2 == *pcVar1;
                                                      pcVar2 = pcVar2 + 1;
                                                      pcVar1 = pcVar1 + 1;
                                                    } while (bVar8);
                                                    if (bVar8) {
                                                      iStack_40 = 0x55;
                                                    }
                                                    else {
                                                      iVar5 = 0xb;
                                                      bVar8 = true;
                                                      pcVar2 = local_30;
                                                      pcVar1 = "texreg2rgb";
                                                      do {
                                                        if (iVar5 == 0) break;
                                                        iVar5 = iVar5 + -1;
                                                        bVar8 = *pcVar2 == *pcVar1;
                                                        pcVar2 = pcVar2 + 1;
                                                        pcVar1 = pcVar1 + 1;
                                                      } while (bVar8);
                                                      if (bVar8) {
                                                        iStack_40 = 0x52;
                                                      }
                                                      else {
                                                        iVar5 = 8;
                                                        bVar8 = true;
                                                        pcVar2 = local_30;
                                                        pcVar1 = "texm3x3";
                                                        do {
                                                          if (iVar5 == 0) break;
                                                          iVar5 = iVar5 + -1;
                                                          bVar8 = *pcVar2 == *pcVar1;
                                                          pcVar2 = pcVar2 + 1;
                                                          pcVar1 = pcVar1 + 1;
                                                        } while (bVar8);
                                                        if (bVar8) {
                                                          iStack_40 = 0x56;
                                                        }
                                                        else {
                                                          iVar5 = 10;
                                                          bVar8 = true;
                                                          pcVar2 = local_30;
                                                          pcVar1 = "texdp3tex";
                                                          do {
                                                            if (iVar5 == 0) break;
                                                            iVar5 = iVar5 + -1;
                                                            bVar8 = *pcVar2 == *pcVar1;
                                                            pcVar2 = pcVar2 + 1;
                                                            pcVar1 = pcVar1 + 1;
                                                          } while (bVar8);
                                                          if (!bVar8) goto LAB__text__0053f141;
                                                          iStack_40 = 0x53;
                                                        }
                                                      }
                                                    }
                                                  }
                                                }
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                                goto LAB__text__0053f2af;
                              }
                              iStack_40 = 0x42;
                            }
                          }
LAB__text__0053f107:
                          uVar3 = 0x105;
                          goto LAB__text__0053ee66;
                        }
                        iVar5 = 6;
                        bVar8 = true;
                        pcVar2 = local_30;
                        pcVar1 = "phase";
                        do {
                          if (iVar5 == 0) break;
                          iVar5 = iVar5 + -1;
                          bVar8 = *pcVar2 == *pcVar1;
                          pcVar2 = pcVar2 + 1;
                          pcVar1 = pcVar1 + 1;
                        } while (bVar8);
                        if (bVar8) {
                          iStack_40 = 0xfffd;
                          goto LAB__text__0053f0bd;
                        }
                        iVar5 = 7;
                        bVar8 = true;
                        pcVar2 = local_30;
                        pcVar1 = "texcrd";
                        do {
                          if (iVar5 == 0) break;
                          iVar5 = iVar5 + -1;
                          bVar8 = *pcVar2 == *pcVar1;
                          pcVar2 = pcVar2 + 1;
                          pcVar1 = pcVar1 + 1;
                        } while (bVar8);
                        if (bVar8) {
                          iStack_40 = 0x40;
                        }
                        else {
                          iVar5 = 8;
                          bVar8 = true;
                          pcVar2 = local_30;
                          pcVar1 = "texkill";
                          do {
                            if (iVar5 == 0) break;
                            iVar5 = iVar5 + -1;
                            bVar8 = *pcVar2 == *pcVar1;
                            pcVar2 = pcVar2 + 1;
                            pcVar1 = pcVar1 + 1;
                          } while (bVar8);
                          if (bVar8) goto LAB__text__0053ef20;
                          iVar5 = 9;
                          bVar8 = true;
                          pcVar2 = local_30;
                          pcVar1 = "texdepth";
                          do {
                            if (iVar5 == 0) break;
                            iVar5 = iVar5 + -1;
                            bVar8 = *pcVar2 == *pcVar1;
                            pcVar2 = pcVar2 + 1;
                            pcVar1 = pcVar1 + 1;
                          } while (bVar8);
                          if (bVar8) {
                            iStack_40 = 0x57;
                            goto LAB__text__0053f107;
                          }
                          iVar5 = 6;
                          bVar8 = true;
                          pcVar2 = local_30;
                          pcVar1 = "texld";
                          do {
                            if (iVar5 == 0) break;
                            iVar5 = iVar5 + -1;
                            bVar8 = *pcVar2 == *pcVar1;
                            pcVar2 = pcVar2 + 1;
                            pcVar1 = pcVar1 + 1;
                          } while (bVar8);
                          if (!bVar8) {
                            bVar8 = true;
                            iVar5 = iStack_40;
                            pcVar2 = local_30;
                            pcVar1 = "bem";
                            do {
                              if (iVar5 == 0) break;
                              iVar5 = iVar5 + -1;
                              bVar8 = *pcVar2 == *pcVar1;
                              pcVar2 = pcVar2 + 1;
                              pcVar1 = pcVar1 + 1;
                            } while (bVar8);
                            if (bVar8) {
                              iStack_40 = 0x59;
                              iVar5 = iStack_40;
                              goto LAB__text__0053f292;
                            }
LAB__text__0053f141:
                            if (*(int *)(local_c + 0xac) != 0) {
                              return 0x109;
                            }
                            goto LAB__text__0053f149;
                          }
                          iStack_40 = 0x42;
                        }
                        goto LAB__text__0053f2af;
                      }
                      iStack_40 = 0x58;
                    }
                  }
LAB__text__0053ee61:
                  uVar3 = 0x108;
                  goto LAB__text__0053ee66;
                }
LAB__text__0053f149:
                bVar8 = true;
                iVar5 = iStack_40;
                pcVar2 = local_30;
                pcVar1 = "rcp";
                do {
                  if (iVar5 == 0) break;
                  iVar5 = iVar5 + -1;
                  bVar8 = *pcVar2 == *pcVar1;
                  pcVar2 = pcVar2 + 1;
                  pcVar1 = pcVar1 + 1;
                } while (bVar8);
                if (bVar8) {
                  iStack_40 = 6;
                }
                else {
                  bVar8 = true;
                  iVar5 = iStack_40;
                  pcVar2 = local_30;
                  pcVar1 = "rsq";
                  do {
                    if (iVar5 == 0) break;
                    iVar5 = iVar5 + -1;
                    bVar8 = *pcVar2 == *pcVar1;
                    pcVar2 = pcVar2 + 1;
                    pcVar1 = pcVar1 + 1;
                  } while (bVar8);
                  if (!bVar8) {
                    bVar8 = true;
                    iVar5 = iStack_40;
                    pcVar2 = local_30;
                    pcVar1 = "min";
                    do {
                      if (iVar5 == 0) break;
                      iVar5 = iVar5 + -1;
                      bVar8 = *pcVar2 == *pcVar1;
                      pcVar2 = pcVar2 + 1;
                      pcVar1 = pcVar1 + 1;
                    } while (bVar8);
                    if (bVar8) {
                      iStack_40 = 10;
                      iVar5 = iStack_40;
                    }
                    else {
                      bVar8 = true;
                      iVar5 = iStack_40;
                      pcVar2 = local_30;
                      pcVar1 = "max";
                      do {
                        if (iVar5 == 0) break;
                        iVar5 = iVar5 + -1;
                        bVar8 = *pcVar2 == *pcVar1;
                        pcVar2 = pcVar2 + 1;
                        pcVar1 = pcVar1 + 1;
                      } while (bVar8);
                      if (bVar8) {
                        iStack_40 = 0xb;
                        iVar5 = iStack_40;
                      }
                      else {
                        bVar8 = true;
                        iVar5 = iStack_40;
                        pcVar2 = local_30;
                        pcVar1 = "slt";
                        do {
                          if (iVar5 == 0) break;
                          iVar5 = iVar5 + -1;
                          bVar8 = *pcVar2 == *pcVar1;
                          pcVar2 = pcVar2 + 1;
                          pcVar1 = pcVar1 + 1;
                        } while (bVar8);
                        if (bVar8) {
                          iStack_40 = 0xc;
                          iVar5 = iStack_40;
                        }
                        else {
                          bVar8 = true;
                          iVar5 = iStack_40;
                          pcVar2 = local_30;
                          pcVar1 = "sge";
                          do {
                            if (iVar5 == 0) break;
                            iVar5 = iVar5 + -1;
                            bVar8 = *pcVar2 == *pcVar1;
                            pcVar2 = pcVar2 + 1;
                            pcVar1 = pcVar1 + 1;
                          } while (bVar8);
                          if (!bVar8) {
                            bVar8 = true;
                            iVar5 = iStack_40;
                            pcVar2 = local_30;
                            pcVar1 = "exp";
                            do {
                              if (iVar5 == 0) break;
                              iVar5 = iVar5 + -1;
                              bVar8 = *pcVar2 == *pcVar1;
                              pcVar2 = pcVar2 + 1;
                              pcVar1 = pcVar1 + 1;
                            } while (bVar8);
                            if (bVar8) {
                              iStack_40 = 0xe;
                            }
                            else {
                              bVar8 = true;
                              iVar5 = iStack_40;
                              pcVar2 = local_30;
                              pcVar1 = "log";
                              do {
                                if (iVar5 == 0) break;
                                iVar5 = iVar5 + -1;
                                bVar8 = *pcVar2 == *pcVar1;
                                pcVar2 = pcVar2 + 1;
                                pcVar1 = pcVar1 + 1;
                              } while (bVar8);
                              if (bVar8) {
                                iStack_40 = 0xf;
                              }
                              else {
                                bVar8 = true;
                                iVar5 = iStack_40;
                                pcVar2 = local_30;
                                pcVar1 = "lit";
                                do {
                                  if (iVar5 == 0) break;
                                  iVar5 = iVar5 + -1;
                                  bVar8 = *pcVar2 == *pcVar1;
                                  pcVar2 = pcVar2 + 1;
                                  pcVar1 = pcVar1 + 1;
                                } while (bVar8);
                                if (!bVar8) {
                                  bVar8 = true;
                                  pcVar2 = local_30;
                                  pcVar1 = "dst";
                                  do {
                                    if (iStack_40 == 0) break;
                                    iStack_40 = iStack_40 + -1;
                                    bVar8 = *pcVar2 == *pcVar1;
                                    pcVar2 = pcVar2 + 1;
                                    pcVar1 = pcVar1 + 1;
                                  } while (bVar8);
                                  if (bVar8) {
                                    iStack_40 = 0x11;
                                    iVar5 = iStack_40;
                                  }
                                  else {
                                    iVar5 = 5;
                                    bVar8 = true;
                                    iVar6 = iVar5;
                                    pcVar2 = local_30;
                                    pcVar1 = "m4x4";
                                    do {
                                      if (iVar6 == 0) break;
                                      iVar6 = iVar6 + -1;
                                      bVar8 = *pcVar2 == *pcVar1;
                                      pcVar2 = pcVar2 + 1;
                                      pcVar1 = pcVar1 + 1;
                                    } while (bVar8);
                                    if (bVar8) {
                                      iStack_40 = 0x14;
                                      iVar5 = iStack_40;
                                    }
                                    else {
                                      bVar8 = true;
                                      iVar6 = iVar5;
                                      pcVar2 = local_30;
                                      pcVar1 = "m4x3";
                                      do {
                                        if (iVar6 == 0) break;
                                        iVar6 = iVar6 + -1;
                                        bVar8 = *pcVar2 == *pcVar1;
                                        pcVar2 = pcVar2 + 1;
                                        pcVar1 = pcVar1 + 1;
                                      } while (bVar8);
                                      if (bVar8) {
                                        iStack_40 = 0x15;
                                        iVar5 = iStack_40;
                                      }
                                      else {
                                        bVar8 = true;
                                        iVar6 = iVar5;
                                        pcVar2 = local_30;
                                        pcVar1 = "m3x4";
                                        do {
                                          if (iVar6 == 0) break;
                                          iVar6 = iVar6 + -1;
                                          bVar8 = *pcVar2 == *pcVar1;
                                          pcVar2 = pcVar2 + 1;
                                          pcVar1 = pcVar1 + 1;
                                        } while (bVar8);
                                        if (bVar8) {
                                          iStack_40 = 0x16;
                                          iVar5 = iStack_40;
                                        }
                                        else {
                                          bVar8 = true;
                                          iVar6 = iVar5;
                                          pcVar2 = local_30;
                                          pcVar1 = "m3x3";
                                          do {
                                            if (iVar6 == 0) break;
                                            iVar6 = iVar6 + -1;
                                            bVar8 = *pcVar2 == *pcVar1;
                                            pcVar2 = pcVar2 + 1;
                                            pcVar1 = pcVar1 + 1;
                                          } while (bVar8);
                                          if (bVar8) {
                                            iStack_40 = 0x17;
                                            iVar5 = iStack_40;
                                          }
                                          else {
                                            bVar8 = true;
                                            iVar6 = iVar5;
                                            pcVar2 = local_30;
                                            pcVar1 = "m3x2";
                                            do {
                                              if (iVar6 == 0) break;
                                              iVar6 = iVar6 + -1;
                                              bVar8 = *pcVar2 == *pcVar1;
                                              pcVar2 = pcVar2 + 1;
                                              pcVar1 = pcVar1 + 1;
                                            } while (bVar8);
                                            if (!bVar8) {
                                              bVar8 = true;
                                              iVar6 = iVar5;
                                              pcVar2 = local_30;
                                              pcVar1 = "expp";
                                              do {
                                                if (iVar6 == 0) break;
                                                iVar6 = iVar6 + -1;
                                                bVar8 = *pcVar2 == *pcVar1;
                                                pcVar2 = pcVar2 + 1;
                                                pcVar1 = pcVar1 + 1;
                                              } while (bVar8);
                                              if (bVar8) {
                                                iStack_40 = 0x4e;
                                              }
                                              else {
                                                bVar8 = true;
                                                pcVar2 = local_30;
                                                pcVar1 = "logp";
                                                do {
                                                  if (iVar5 == 0) break;
                                                  iVar5 = iVar5 + -1;
                                                  bVar8 = *pcVar2 == *pcVar1;
                                                  pcVar2 = pcVar2 + 1;
                                                  pcVar1 = pcVar1 + 1;
                                                } while (bVar8);
                                                if (!bVar8) {
                                                  return 0x109;
                                                }
                                                iStack_40 = 0x4f;
                                              }
                                              goto LAB__text__0053f2af;
                                            }
                                            iStack_40 = 0x18;
                                            iVar5 = iStack_40;
                                          }
                                        }
                                      }
                                    }
                                  }
                                  goto LAB__text__0053f292;
                                }
                                iStack_40 = 0x10;
                              }
                            }
                            goto LAB__text__0053f2af;
                          }
                          iStack_40 = 0xd;
                          iVar5 = iStack_40;
                        }
                      }
                    }
                    goto LAB__text__0053f292;
                  }
                  iStack_40 = 7;
                }
              }
LAB__text__0053f2af:
              uVar3 = 0x106;
              goto LAB__text__0053ee66;
            }
            iStack_40 = 9;
            iVar5 = iStack_40;
          }
        }
      }
    }
LAB__text__0053f292:
    iStack_40 = iVar5;
    uVar3 = 0x107;
  }
LAB__text__0053ee66:
  if (local_10 != (char *)0x0) {
    if (*(int *)(local_c + 0xac) == 0) {
      return 0x109;
    }
    uVar7 = (int)local_18 - (int)local_10;
    local_20 = uVar7;
    if (0xf < uVar7) {
      return 0x109;
    }
    pcVar2 = local_10;
    pcVar1 = local_30;
    for (uVar4 = uVar7 >> 2; uVar4 != 0; uVar4 = uVar4 - 1) {
      *(undefined4 *)pcVar1 = *(undefined4 *)pcVar2;
      pcVar2 = pcVar2 + 4;
      pcVar1 = pcVar1 + 4;
    }
    for (uVar4 = uVar7 & 3; uVar4 != 0; uVar4 = uVar4 - 1) {
      *pcVar1 = *pcVar2;
      pcVar2 = pcVar2 + 1;
      pcVar1 = pcVar1 + 1;
    }
    local_30[uVar7] = '\0';
    iVar5 = 3;
    bVar8 = true;
    pcVar2 = local_30;
    pcVar1 = "x8";
    do {
      if (iVar5 == 0) break;
      iVar5 = iVar5 + -1;
      bVar8 = *pcVar2 == *pcVar1;
      pcVar2 = pcVar2 + 1;
      pcVar1 = pcVar1 + 1;
    } while (bVar8);
    if (bVar8) {
      local_8 = 0x3000000;
    }
    else {
      iVar5 = 3;
      bVar8 = true;
      pcVar2 = local_30;
      pcVar1 = "x4";
      do {
        if (iVar5 == 0) break;
        iVar5 = iVar5 + -1;
        bVar8 = *pcVar2 == *pcVar1;
        pcVar2 = pcVar2 + 1;
        pcVar1 = pcVar1 + 1;
      } while (bVar8);
      if (bVar8) {
        local_8 = 0x2000000;
      }
      else {
        iVar5 = 3;
        bVar8 = true;
        pcVar2 = local_30;
        pcVar1 = "x2";
        do {
          if (iVar5 == 0) break;
          iVar5 = iVar5 + -1;
          bVar8 = *pcVar2 == *pcVar1;
          pcVar2 = pcVar2 + 1;
          pcVar1 = pcVar1 + 1;
        } while (bVar8);
        if (bVar8) {
          local_8 = 0x1000000;
        }
        else {
          iVar5 = 3;
          bVar8 = true;
          pcVar2 = local_30;
          pcVar1 = "d2";
          do {
            if (iVar5 == 0) break;
            iVar5 = iVar5 + -1;
            bVar8 = *pcVar2 == *pcVar1;
            pcVar2 = pcVar2 + 1;
            pcVar1 = pcVar1 + 1;
          } while (bVar8);
          if (bVar8) {
            local_8 = 0xf000000;
          }
          else {
            iVar5 = 3;
            bVar8 = true;
            pcVar2 = local_30;
            pcVar1 = "d4";
            do {
              if (iVar5 == 0) break;
              iVar5 = iVar5 + -1;
              bVar8 = *pcVar2 == *pcVar1;
              pcVar2 = pcVar2 + 1;
              pcVar1 = pcVar1 + 1;
            } while (bVar8);
            if (bVar8) {
              local_8 = 0xe000000;
            }
            else {
              iVar5 = 3;
              bVar8 = true;
              pcVar2 = local_30;
              pcVar1 = "d8";
              do {
                if (iVar5 == 0) break;
                iVar5 = iVar5 + -1;
                bVar8 = *pcVar2 == *pcVar1;
                pcVar2 = pcVar2 + 1;
                pcVar1 = pcVar1 + 1;
              } while (bVar8);
              if (bVar8) {
                local_8 = 0xd000000;
              }
              else {
                if (local_14 != (char *)0x0) {
                  return 0x109;
                }
                local_14 = local_10;
                local_1c = local_18;
              }
            }
          }
        }
      }
    }
  }
  if (local_14 == (char *)0x0) {
LAB__text__0053f3c8:
    *(int *)(local_c + 0x1c8) = iStack_40;
    *(uint *)(local_c + 0x1cc) = local_8;
    return uVar3;
  }
  if (*(int *)(local_c + 0xac) != 0) {
    uVar7 = (int)local_1c - (int)local_14;
    local_20 = uVar7;
    if (uVar7 < 0x10) {
      pcVar2 = local_14;
      pcVar1 = local_30;
      for (uVar4 = uVar7 >> 2; uVar4 != 0; uVar4 = uVar4 - 1) {
        *(undefined4 *)pcVar1 = *(undefined4 *)pcVar2;
        pcVar2 = pcVar2 + 4;
        pcVar1 = pcVar1 + 4;
      }
      for (uVar4 = uVar7 & 3; uVar4 != 0; uVar4 = uVar4 - 1) {
        *pcVar1 = *pcVar2;
        pcVar2 = pcVar2 + 1;
        pcVar1 = pcVar1 + 1;
      }
      local_30[uVar7] = '\0';
      iVar5 = 4;
      bVar8 = true;
      pcVar2 = local_30;
      pcVar1 = "sat";
      do {
        if (iVar5 == 0) break;
        iVar5 = iVar5 + -1;
        bVar8 = *pcVar2 == *pcVar1;
        pcVar2 = pcVar2 + 1;
        pcVar1 = pcVar1 + 1;
      } while (bVar8);
      if (bVar8) {
        local_8 = local_8 | 0x100000;
        goto LAB__text__0053f3c8;
      }
    }
  }
  return 0x109;
}

