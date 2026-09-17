
int FUN__text__00572aa0(int param_1,char *param_2)

{
  char *pcVar1;
  int iVar2;
  size_t sVar3;
  size_t sVar4;
  int local_b4;
  int local_b0;
  int local_ac;
  char *local_a0;
  char local_9c [132];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  if ((param_1 < 0) || (5 < param_1)) {
    local_c = 0;
  }
  else {
    FUN__text__00577040(0x13);
    local_8 = 1;
    DAT_0080bb68 = DAT_0080bb68 + 1;
    while (DAT_0080bb6c != 0) {
      (*DAT_00592264)(1);
    }
    if (param_1 == 0) {
      local_18 = 1;
      local_10 = 0;
      if (param_2 == (char *)0x0) {
        local_c = FUN__text__00573030();
      }
      else if (((*param_2 == 'L') && (param_2[1] == 'C')) && (param_2[2] == '_')) {
        local_a0 = param_2;
        do {
          pcVar1 = (char *)FUN__text__00581f50(local_a0,&DAT_005f9db0);
          if (((pcVar1 == (char *)0x0) || (sVar4 = (int)pcVar1 - (int)local_a0, sVar4 == 0)) ||
             (*pcVar1 == ';')) {
            if (local_8 != 0) {
              FUN__text__005770e0(0x13);
              DAT_0080bb68 = DAT_0080bb68 + -1;
            }
            return 0;
          }
          local_14 = 1;
          while ((local_14 < 6 &&
                 ((iVar2 = _strncmp(*(char **)(&UNK_00761b28 + local_14 * 0xc),local_a0,sVar4),
                  iVar2 != 0 ||
                  (sVar3 = _strlen(*(char **)(&UNK_00761b28 + local_14 * 0xc)), sVar4 != sVar3)))))
          {
            local_14 = local_14 + 1;
          }
          pcVar1 = pcVar1 + 1;
          sVar4 = FUN__text__00581f10(pcVar1,&DAT_005f9dac);
          if ((sVar4 == 0) && (*pcVar1 != ';')) {
            if (local_8 != 0) {
              FUN__text__005770e0(0x13);
              DAT_0080bb68 = DAT_0080bb68 + -1;
            }
            return 0;
          }
          if (local_14 < 6) {
            _strncpy(local_9c,pcVar1,sVar4);
            local_9c[sVar4] = '\0';
            iVar2 = FUN__text__00572e90(local_14,local_9c);
            if (iVar2 != 0) {
              local_10 = local_10 + 1;
            }
          }
          local_a0 = pcVar1 + sVar4;
          if (*local_a0 != '\0') {
            local_a0 = local_a0 + 1;
          }
        } while (*local_a0 != '\0');
        if (local_10 == 0) {
          local_b0 = 0;
        }
        else {
          local_b0 = FUN__text__00573030();
        }
        local_c = local_b0;
      }
      else {
        local_c = FUN__text__00573130(param_2,local_9c,0,0,0);
        if (local_c != 0) {
          for (local_14 = 0; local_14 < 6; local_14 = local_14 + 1) {
            if (local_14 != 0) {
              iVar2 = _strcmp(local_9c,(char *)(&DAT_00761b2c)[local_14 * 3]);
              if (iVar2 == 0) {
                local_10 = local_10 + 1;
              }
              else {
                iVar2 = FUN__text__00572e90(local_14,local_9c);
                if (iVar2 == 0) {
                  local_18 = 0;
                }
                else {
                  local_10 = local_10 + 1;
                }
              }
            }
          }
          if (local_18 == 0) {
            if (local_10 == 0) {
              local_b4 = 0;
            }
            else {
              local_b4 = FUN__text__00573030();
            }
            local_c = local_b4;
          }
          else {
            local_c = FUN__text__00573030();
            __free_dbg(DAT_00761b2c,2);
            DAT_00761b2c = 0;
          }
        }
      }
    }
    else {
      if (param_2 == (char *)0x0) {
        local_ac = (&DAT_00761b2c)[param_1 * 3];
      }
      else {
        local_ac = FUN__text__00572e90(param_1,param_2);
      }
      local_c = local_ac;
    }
    if (local_8 != 0) {
      FUN__text__005770e0(0x13);
      DAT_0080bb68 = DAT_0080bb68 + -1;
    }
  }
  return local_c;
}

