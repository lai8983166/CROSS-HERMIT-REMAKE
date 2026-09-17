
void __fastcall FUN__text__00445c10(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_60 [16];
  int local_20;
  int *local_1c;
  int local_18;
  int local_14;
  int local_10;
  undefined4 local_c;
  int local_8;
  
  puVar3 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = 0;
  local_18 = param_1 + 0x1a54;
  local_20 = *(int *)(param_1 + 0x1bb4);
  local_8 = param_1;
  if (local_20 == 0) {
    local_1c = (int *)FUN__text__00418780();
    if (*local_1c == 0) {
      *(undefined4 *)(local_8 + 0x1bb0) = 0;
    }
    else {
      local_10 = FUN__text__00428310();
      if ((*local_1c <= local_10) &&
         (iVar2 = FUN__text__00424f80("NowSession < se->cnt",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                      DAT_00606720 + 0x11,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      if (local_10 == -1) {
        *(undefined4 *)(local_8 + 0x1bb4) = 0;
      }
      else {
        *(undefined4 *)(local_8 + 0x1bc0) = 1;
        *(int *)(local_8 + 0x1bb4) = *(int *)(local_8 + 0x1bb4) + 1;
      }
    }
  }
  else if (local_20 == 1) {
    if (*(int *)(param_1 + 0x1bc0) == 0) {
      *(int *)(param_1 + 0x1bb4) = *(int *)(param_1 + 0x1bb4) + 1;
    }
    else {
      *(int *)(param_1 + 0x1bc0) = *(int *)(param_1 + 0x1bc0) + -1;
    }
  }
  else if (local_20 == 2) {
    local_1c = (int *)FUN__text__00418780();
    local_10 = FUN__text__00428310();
    if (*(int *)(local_8 + 0x34) == local_1c[local_10 * 0x15 + 0x13]) {
      local_14 = FUN__text__004190f0(local_10,*(undefined4 *)(local_8 + 0x34));
      if (local_14 == 0) {
        local_14 = FUN__text__004199a0(local_18 + 0xc,0);
        if (local_14 == 0) {
          *(undefined4 *)(local_8 + 0x1a50) = 9;
          local_c = 1;
          local_14 = 0;
        }
        else {
          local_14 = FUN__text__00419240();
          if (local_14 == 0) {
            *(undefined4 *)(local_8 + 0x1bb0) = 0;
          }
          else {
            *(undefined4 *)(local_8 + 0x1bb0) = 0xff;
            *(undefined4 *)(local_8 + 0x1bc4) = 5;
            *(undefined4 *)(local_8 + 0x1bc8) = 1;
          }
        }
      }
      else {
        *(undefined4 *)(local_8 + 0x1bb0) = 0xff;
        *(undefined4 *)(local_8 + 0x1bc4) = 4;
      }
    }
    else {
      *(undefined4 *)(local_8 + 0x1bb0) = 0xff;
      *(undefined4 *)(local_8 + 0x1bc4) = 7;
    }
  }
  FUN__text__00446340(0xffffffff,0xff);
  FUN__text__0044ca80();
  FUN__text__0044c9a0(0);
  local_8 = 0x445eab;
  FUN__text__0056ce80();
  return;
}

