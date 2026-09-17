
void FUN__text__00479f40(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  char local_18;
  char local_14;
  char *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1 + 0x290;
  local_10 = (char *)(param_1 + 0x293);
  local_14 = *local_10;
  if (local_14 == '\0') {
    FUN__text__0046b0b0(param_1,0);
    FUN__text__0046b0f0(param_1,0);
    *(undefined2 *)(param_1 + 10) = 0;
    *local_10 = *local_10 + '\x01';
  }
  else if (local_14 != '\x01') goto LAB__text__0047a224;
  local_18 = *(char *)(*(int *)(param_1 + 600) + 0xf);
  if (local_18 == '\x02') {
    iVar2 = FUN__text__00468eb0(param_1);
    if (iVar2 != 0) {
      FUN__text__00472370(param_1);
    }
  }
  else if (local_18 == '\x03') {
    iVar2 = FUN__text__00468eb0(param_1);
    if (iVar2 == 0) {
      iVar2 = FUN__text__00469ad0(param_1);
      if (iVar2 == 0) {
        if ((*(char *)(*(int *)(param_1 + 600) + 0x96) == '\x03') &&
           (*(char *)(*(int *)(param_1 + 600) + 0x97) != '\0')) {
          if (*(byte *)(*(int *)(param_1 + 600) + 0x97) < 99) {
            *(char *)(*(int *)(param_1 + 600) + 0x97) =
                 *(char *)(*(int *)(param_1 + 600) + 0x97) + -1;
          }
          *(undefined2 *)(*(int *)(param_1 + 600) + 0x16) =
               *(undefined2 *)(*(int *)(param_1 + 600) + 0x14);
          *(undefined2 *)(*(int *)(param_1 + 600) + 0x1c) =
               *(undefined2 *)(*(int *)(param_1 + 600) + 0x1a);
          *(undefined4 *)(*(int *)(param_1 + 600) + 0x24) =
               *(undefined4 *)(*(int *)(param_1 + 600) + 0x20);
          *(undefined1 *)(*(int *)(param_1 + 600) + 0xf) = 2;
        }
        else {
          *(undefined1 *)(*(int *)(param_1 + 600) + 0xf) = 4;
        }
      }
      else {
        *(undefined1 *)(*(int *)(param_1 + 600) + 0xf) = 4;
      }
    }
    else {
      if (*(short *)(*(int *)(param_1 + 600) + 0x16) == 0) {
        *(undefined2 *)(*(int *)(param_1 + 600) + 0x16) = 1;
      }
      FUN__text__00472370(param_1);
      if (*(short *)(*(int *)(param_1 + 600) + 0x14) <= *(short *)(*(int *)(param_1 + 600) + 0x16))
      {
        *(undefined2 *)(*(int *)(param_1 + 600) + 0x16) =
             *(undefined2 *)(*(int *)(param_1 + 600) + 0x14);
        *(undefined2 *)(*(int *)(param_1 + 600) + 0x1c) =
             *(undefined2 *)(*(int *)(param_1 + 600) + 0x1a);
        *(undefined1 *)(*(int *)(param_1 + 600) + 0xf) = 2;
        FUN__text__0049ad90(param_1,0x96);
      }
    }
  }
  else if (local_18 == '\x04') {
    if ((*(int *)(param_1 + 0x2f8) != 0) &&
       (iVar2 = FUN__text__00424f80(&DAT_0059d4b8,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618e24 + 0x49,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if ((*(int *)(param_1 + 0x3e4) != 0) &&
       (iVar2 = FUN__text__00424f80(&DAT_0059d474,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618e24 + 0x4a,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
LAB__text__0047a224:
  local_8 = 0x47a236;
  FUN__text__0056ce80();
  return;
}

