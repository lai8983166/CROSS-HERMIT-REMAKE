
void __fastcall FUN__text__00454cf0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  char *local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (char *)(param_1 + 0x44);
  local_8 = param_1;
  iVar1 = FUN__text__00454c40();
  if (iVar1 != 0) {
    FUN__text__00457830();
    local_14 = (int)*local_c;
    switch(local_14) {
    case 0:
      local_c[0x18] = '\0';
      local_c[0x19] = '\0';
      local_c[0x1a] = '\0';
      local_c[0x1b] = '\0';
      *local_c = *local_c + '\x01';
      break;
    case 1:
      *local_c = *local_c + '\x01';
      break;
    case 2:
      if (*(int *)(local_c + 4) == 1) {
        local_10 = FUN__text__004ce8f0();
      }
      else {
        local_10 = 0;
      }
      if (local_10 == 0) {
        *local_c = *local_c + '\x01';
        local_c[0x15] = '\x02';
        if (*(int *)(local_c + 0xc) == 0) {
          *local_c = '\x04';
        }
      }
      FUN__text__004563d0();
      break;
    case 3:
      if (local_c[0x14] != '\0') {
        local_c[0x14] = '\0';
        *local_c = *local_c + '\x01';
        iVar1 = FUN__text__00497c50();
        if (iVar1 == 0) {
          *local_c = *local_c + '\x01';
        }
        else {
          FUN__text__00497980(0x3c);
        }
      }
      break;
    case 4:
      iVar1 = FUN__text__00497c50();
      if (iVar1 == 0) {
        FUN__text__00454ee0();
        *local_c = *local_c + '\x01';
      }
      break;
    case 5:
      local_c[0x15] = '\x03';
      if (*(int *)(local_8 + 0x4c) == 1) {
        *(undefined1 *)(local_8 + 0x171) = 1;
        *(undefined1 *)(local_8 + 0x172) = 1;
        *local_c = *local_c + '\x01';
      }
      else {
        if (*(int *)(local_8 + 0x54) == 1) {
          FUN__text__00467850(1,1);
        }
        *(undefined1 *)(local_8 + 0x43) = 0;
      }
      FUN__text__0041f710();
      goto LAB__text__00454eb1;
    }
    FUN__text__00497aa0();
    FUN__text__00498310();
  }
LAB__text__00454eb1:
  local_8 = 0x454ebe;
  FUN__text__0056ce80();
  return;
}

