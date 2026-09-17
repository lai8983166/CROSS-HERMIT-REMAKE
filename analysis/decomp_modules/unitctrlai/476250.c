
void __thiscall FUN__text__00476250(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  char local_1c;
  char local_18;
  short local_14;
  char *local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_2 + 0x290;
  local_10 = (char *)(param_2 + 0x293);
  local_18 = *local_10;
  local_8 = param_1;
  if (local_18 == '\0') {
    FUN__text__0046bcc0(param_2,1);
    *local_10 = *local_10 + '\x01';
  }
  else if (local_18 != '\x01') {
    if (local_18 == '\x02') {
      iVar1 = FUN__text__00468d80(param_2);
      if (iVar1 == 0) {
        iVar1 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618dfc + 0x14);
        local_14 = (short)(iVar1 % 10) * 0x14 + 0x1e;
      }
      else {
        local_14 = 0x3c;
      }
      if (local_14 < *(short *)(param_2 + 10)) {
        if (*(char *)(*(int *)(param_2 + 600) + 0xa4) == '\a') {
          *local_10 = *local_10 + '\x01';
        }
        else {
          iVar1 = FUN__text__00468d80(param_2);
          if ((iVar1 == 0) ||
             (local_1c = *(char *)(*(int *)(param_2 + 600) + 0x9f), local_1c != '\x03')) {
            FUN__text__00475270(param_2,0xf);
          }
          else {
            FUN__text__00475270(param_2,3);
          }
          *local_10 = *local_10 + '\x01';
        }
      }
    }
    goto LAB__text__004763bc;
  }
  if (*(char *)(local_8 + 0x108b48) == '\0') {
    *(undefined2 *)(param_2 + 10) = 0;
    *local_10 = *local_10 + '\x01';
  }
LAB__text__004763bc:
  local_8 = 0x4763c9;
  FUN__text__0056ce80();
  return;
}

