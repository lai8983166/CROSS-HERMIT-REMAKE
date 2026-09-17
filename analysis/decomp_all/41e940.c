
void __fastcall FUN__text__0041e940(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  int local_24;
  undefined4 local_20;
  undefined4 local_1c;
  int local_18;
  undefined4 local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_18 = 0;
  local_8 = param_1;
  if (*(int *)(param_1 + 0x14) != 0) {
    while( true ) {
      (**(code **)(**(int **)(local_8 + 0x14) + 0x20))
                (*(undefined4 *)(local_8 + 0x14),&local_c,&local_10,&local_14,0);
      iVar1 = FUN__text__0056ce80();
      if (iVar1 < 0) break;
      (**(code **)(**(int **)(local_8 + 0x14) + 0x30))
                (*(undefined4 *)(local_8 + 0x14),local_c,local_10,local_14);
      local_18 = FUN__text__0056ce80();
      local_24 = local_c;
      if (local_c == 1) {
        if (*(int *)(local_8 + 0x248) == 1) {
          local_20 = 0;
          local_1c = 0;
          (**(code **)(**(int **)(local_8 + 8) + 0x38))
                    (*(undefined4 *)(local_8 + 8),&local_20,1,0,0);
          local_18 = FUN__text__0056ce80();
          if ((local_18 < 0) && (*(int *)(local_8 + 4) != 0)) {
            (**(code **)(**(int **)(local_8 + 4) + 0x24))(*(undefined4 *)(local_8 + 4));
            local_18 = FUN__text__0056ce80();
            if (local_18 < 0) {
              *(undefined1 *)(local_8 + 0x22) = 0;
              *(undefined1 *)(local_8 + 0x21) = 0;
            }
            else {
              (**(code **)(**(int **)(local_8 + 4) + 0x1c))(*(undefined4 *)(local_8 + 4));
              local_18 = FUN__text__0056ce80();
              if (local_18 < 0) {
                *(undefined1 *)(local_8 + 0x22) = 0;
                *(undefined1 *)(local_8 + 0x21) = 0;
              }
            }
          }
        }
        else {
          *(undefined1 *)(local_8 + 0x22) = 0;
          *(undefined1 *)(local_8 + 0x21) = 0;
        }
      }
    }
  }
  local_8 = 0x41eac4;
  FUN__text__0056ce80();
  return;
}

