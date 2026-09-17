
void __fastcall FUN__text__0046f440(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  undefined4 local_24;
  undefined4 local_20;
  undefined2 local_1c [2];
  undefined2 local_18 [2];
  int *local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  _memset((void *)(param_1 + 0x3098c),0,10);
  *(undefined2 *)(local_8 + 0x30992) = 0xffff;
  if (*(char *)(local_8 + 0x108b38) != '\0') {
    if (*(int *)(local_8 + 0x2f150) == 1) {
      *(undefined1 *)(local_8 + 0x30994) = 0;
    }
    else {
      iVar2 = FUN__text__00458100();
      if (iVar2 == 0) {
        if (*(int *)(local_8 + 0x2a350) == 1) {
          *(undefined1 *)(local_8 + 0x3098c) = 1;
          *(undefined1 *)(local_8 + 0x3098d) = 100;
          *(short *)(local_8 + 0x3098e) =
               (short)((int)((int)*(short *)(local_8 + 0x2a354) +
                            ((int)*(short *)(local_8 + 0x2a354) >> 0x1f & 0x1fU)) >> 5);
          *(short *)(local_8 + 0x30990) =
               (short)((int)((int)*(short *)(local_8 + 0x2a356) +
                            ((int)*(short *)(local_8 + 0x2a356) >> 0x1f & 0xfU)) >> 4);
          *(undefined1 *)(local_8 + 0x30994) = 0;
        }
        else {
          if (*(int *)(local_8 + 0x2a348) == 1) {
            *(undefined1 *)(local_8 + 0x3098c) = 1;
          }
          for (local_c = 0; local_c != *(int *)(local_8 + 0xdc30c); local_c = local_c + 1) {
            local_10 = FUN__text__0046fc20(*(undefined4 *)(local_8 + 0xdc310 + local_c * 4));
            if (local_10 != 0) {
              local_20 = FUN__text__0046a950(*(undefined4 *)(local_8 + 0xdc310 + local_c * 4));
              switch(local_20) {
              case 0:
                *(undefined1 *)(local_8 + 0x3098d) = 1;
                break;
              case 1:
                *(undefined1 *)(local_8 + 0x3098d) = 2;
                break;
              case 2:
                *(undefined1 *)(local_8 + 0x3098d) = 4;
                break;
              case 3:
                *(undefined1 *)(local_8 + 0x3098d) = 5;
                break;
              case 4:
                *(undefined1 *)(local_8 + 0x3098d) = 3;
                break;
              default:
                iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                            "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                            DAT_00618c2c + 0x31,0);
                if (iVar2 != 0) {
                  pcVar1 = (code *)swi(3);
                  (*pcVar1)();
                  return;
                }
              }
              *(undefined2 *)(local_8 + 0x30992) =
                   *(undefined2 *)(*(int *)(local_8 + 0xdc310 + local_c * 4) + 2);
              break;
            }
          }
          if (*(char *)(local_8 + 0x3098c) != '\0') {
            *(short *)(local_8 + 0x3098e) =
                 (short)((int)((int)*(short *)(local_8 + 0x2a34c) +
                              ((int)*(short *)(local_8 + 0x2a34c) >> 0x1f & 0x1fU)) >> 5);
            *(short *)(local_8 + 0x30990) =
                 (short)((int)((int)*(short *)(local_8 + 0x2a34e) +
                              ((int)*(short *)(local_8 + 0x2a34e) >> 0x1f & 0xfU)) >> 4);
            if (*(short *)(local_8 + 0x30992) == -1) {
              iVar2 = FUN__text__0046b130((int)*(short *)(local_8 + 0x2a34c) -
                                          (int)*(short *)(local_8 + 0x2a30e),
                                          ((int)*(short *)(local_8 + 0x2a34e) -
                                          (int)*(short *)(local_8 + 0x2a310)) + 0x1e);
              if (iVar2 == 0) {
                iVar2 = FUN__text__00440d40(*(undefined2 *)(local_8 + 0x2a34c),
                                            *(undefined2 *)(local_8 + 0x2a34e));
                if (iVar2 != 0) {
                  local_18[0] = *(undefined2 *)(local_8 + 0x2a34c);
                  local_1c[0] = *(undefined2 *)(local_8 + 0x2a34e);
                  FUN__text__00440dd0(local_18,local_1c);
                  local_14 = (int *)(local_8 + 0xdc8ec);
                  for (local_c = 0; local_c != *local_14; local_c = local_c + 1) {
                    iVar2 = FUN__text__0046fc20(local_14[local_c + 1]);
                    if (iVar2 != 0) {
                      local_24 = FUN__text__0046a950(local_8 + 0x80aec + local_c * 0x520);
                      switch(local_24) {
                      case 0:
                        *(undefined1 *)(local_8 + 0x3098d) = 1;
                        break;
                      case 1:
                        *(undefined1 *)(local_8 + 0x3098d) = 2;
                        break;
                      case 2:
                        *(undefined1 *)(local_8 + 0x3098d) = 4;
                        break;
                      case 3:
                        *(undefined1 *)(local_8 + 0x3098d) = 5;
                        break;
                      case 4:
                        *(undefined1 *)(local_8 + 0x3098d) = 3;
                        break;
                      default:
                        iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                                                                                        
                                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp"
                                                  ,DAT_00618c2c + 0x5e,0);
                        if (iVar2 != 0) {
                          pcVar1 = (code *)swi(3);
                          (*pcVar1)();
                          return;
                        }
                      }
                      break;
                    }
                  }
                }
              }
              else {
                *(undefined1 *)(local_8 + 0x3098d) = 100;
                *(short *)(local_8 + 0x3098e) =
                     (short)((int)((int)*(short *)(local_8 + 0x2a34c) +
                                  ((int)*(short *)(local_8 + 0x2a34c) >> 0x1f & 0x1fU)) >> 5);
                *(short *)(local_8 + 0x30990) =
                     (short)((int)((int)*(short *)(local_8 + 0x2a34e) +
                                  ((int)*(short *)(local_8 + 0x2a34e) >> 0x1f & 0xfU)) >> 4);
              }
            }
          }
        }
      }
      else {
        FUN__text__00493c40();
      }
    }
  }
  local_8 = 0x46f87b;
  FUN__text__0056ce80();
  return;
}

