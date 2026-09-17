
void __thiscall FUN__text__00493450(undefined4 param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  char local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_2 + 0x510) != 0) {
    local_c = *(int *)(param_2 + 0x510);
    local_8 = param_1;
    while (local_c != 0) {
      local_14 = *(char *)(local_c + 1);
      if (local_14 == '\0') {
        FUN__text__00472550(param_2,0,(int)*(short *)(local_c + 2));
      }
      else if (local_14 == '\x01') {
        FUN__text__00472550(param_2,1,(int)*(short *)(local_c + 2));
      }
      else if (local_14 == '\x02') {
        FUN__text__00472550(param_2,2,(int)*(short *)(local_c + 2));
      }
      else {
        iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlDamage.cpp",
                                    DAT_00619278 + 0x15,0);
        if (iVar2 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
      local_10 = *(int *)(local_c + 4);
      FUN__text__00492f00(local_c);
      local_c = local_10;
    }
    *(undefined4 *)(param_2 + 0x510) = 0;
  }
  local_8 = 0x49355f;
  FUN__text__0056ce80();
  return;
}

