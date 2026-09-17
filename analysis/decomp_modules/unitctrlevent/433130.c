
void FUN__text__00433130(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = FUN__text__00431dd0(&DAT_005ff760);
  iVar2 = FUN__text__004e2720(3,0);
  if (iVar2 == 0) goto LAB__text__00433220;
  local_c = FUN__text__00431d40((int)DAT_005ff760);
  iVar2 = FUN__text__0046a550(local_c);
  if (iVar2 == 0) goto LAB__text__00433220;
  FUN__text__004e29a0(3,0,0);
  FUN__text__004e29a0(1,0,(int)*(short *)(local_c + 2));
LAB__text__004331ba:
  do {
    local_10 = FUN__text__004e2720(2,0);
    local_10 = local_10 + -1;
    FUN__text__004e29a0(2,0,local_10);
    if ((local_10 < 0) &&
       (iVar2 = FUN__text__00424f80("0 <= cnt",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent003.cpp",
                                    DAT_005ff768 + 0x14,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    FUN__text__00454bb0(0,0,0x17);
LAB__text__00433220:
    iVar2 = FUN__text__004e2720(3,1);
    if (iVar2 != 0) {
      local_c = FUN__text__00431d40((int)DAT_005ff762);
      iVar2 = FUN__text__0046a550(local_c);
      if (iVar2 != 0) {
        FUN__text__004e29a0(3,1,0);
        FUN__text__004e29a0(1,0,(int)*(short *)(local_c + 2));
        goto LAB__text__004331ba;
      }
    }
    iVar2 = FUN__text__004e2720(3,2);
    if (iVar2 == 0) {
LAB__text__004332d4:
      local_c = FUN__text__00431d40((int)DAT_005ff760);
      iVar2 = FUN__text__0046a430(local_c);
      if (((iVar2 == 0) || (iVar2 = FUN__text__004e2720(3,0), iVar2 != 0)) ||
         (iVar2 = FUN__text__004335b0(), iVar2 == 0)) {
        local_c = FUN__text__00431d40((int)DAT_005ff762);
        iVar2 = FUN__text__0046a430(local_c);
        if (((iVar2 == 0) || (iVar2 = FUN__text__004e2720(3,1), iVar2 != 0)) ||
           (iVar2 = FUN__text__004335b0(), iVar2 == 0)) {
          local_c = FUN__text__00431d40((int)DAT_005ff764);
          iVar2 = FUN__text__0046a430(local_c);
          if (((iVar2 == 0) || (iVar2 = FUN__text__004e2720(3,2), iVar2 != 0)) ||
             (iVar2 = FUN__text__004335b0(), iVar2 == 0)) {
            local_10 = 0;
            if ((2 < local_14) && (iVar2 = FUN__text__004307b0(), iVar2 != 0)) {
              iVar2 = FUN__text__004e2720(2,0);
              if (iVar2 == 3) {
                FUN__text__004e29a0(1,0,0xff);
              }
              else {
                iVar2 = FUN__text__004e2720(3,0);
                if (iVar2 == 0) {
                  local_c = FUN__text__00431d40((int)DAT_005ff760);
                }
                else {
                  iVar2 = FUN__text__004e2720(3,1);
                  if (iVar2 == 0) {
                    local_c = FUN__text__00431d40((int)DAT_005ff762);
                  }
                  else {
                    iVar2 = FUN__text__004e2720(3,2);
                    if (iVar2 == 0) {
                      local_c = FUN__text__00431d40((int)DAT_005ff764);
                    }
                    else {
                      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent003.cpp"
                                                  ,DAT_005ff768 + 100,0);
                      if (iVar2 != 0) {
                        pcVar1 = (code *)swi(3);
                        (*pcVar1)();
                        return;
                      }
                    }
                  }
                }
                FUN__text__004e29a0(1,0,(int)*(short *)(local_c + 2));
              }
              iVar2 = FUN__text__00430ba0();
              if (iVar2 == 0) {
                FUN__text__00454af0(5,5);
              }
              else {
                FUN__text__00454af0(2,5);
              }
            }
            if (*(int *)(local_8 + 0x2e6f4) == 0) {
              if ((local_14 < 3) && (iVar2 = FUN__text__004307b0(), iVar2 == 0)) {
                FUN__text__00454ab0(0xb);
              }
              else {
                FUN__text__00454af0(8,5);
              }
            }
            else {
              iVar2 = FUN__text__00430df0();
              if (iVar2 != 0) {
                FUN__text__00454ab0(0xe);
              }
            }
          }
          else {
            FUN__text__004e29a0(3,2,1);
            FUN__text__004e29a0(1,0,(int)*(short *)(local_c + 2));
          }
        }
        else {
          FUN__text__004e29a0(3,1,1);
          FUN__text__004e29a0(1,0,(int)*(short *)(local_c + 2));
        }
      }
      else {
        FUN__text__004e29a0(3,0,1);
        FUN__text__004e29a0(1,0,(int)*(short *)(local_c + 2));
      }
      local_8 = 0x4335ab;
      FUN__text__0056ce80();
      return;
    }
    local_c = FUN__text__00431d40((int)DAT_005ff764);
    iVar2 = FUN__text__0046a550(local_c);
    if (iVar2 == 0) goto LAB__text__004332d4;
    FUN__text__004e29a0(3,2,0);
    FUN__text__004e29a0(1,0,(int)*(short *)(local_c + 2));
  } while( true );
}

