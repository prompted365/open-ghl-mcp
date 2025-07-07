export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instanciate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "12.2.3 (519615d)"
  }
  graphql_public: {
    Tables: {
      [_ in never]: never
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      graphql: {
        Args: {
          operationName?: string
          query?: string
          variables?: Json
          extensions?: Json
        }
        Returns: Json
      }
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
  public: {
    Tables: {
      audit_logs: {
        Row: {
          created_at: string
          event_type: string
          group_id: string | null
          id: string
          metadata: Json | null
          related_table: string | null
          user_id: string | null
        }
        Insert: {
          created_at?: string
          event_type: string
          group_id?: string | null
          id?: string
          metadata?: Json | null
          related_table?: string | null
          user_id?: string | null
        }
        Update: {
          created_at?: string
          event_type?: string
          group_id?: string | null
          id?: string
          metadata?: Json | null
          related_table?: string | null
          user_id?: string | null
        }
        Relationships: []
      }
      clients: {
        Row: {
          address: string | null
          city: string | null
          created_at: string | null
          email: string | null
          estimated_annual_usage_kwh: number | null
          group_id: string
          id: string
          name: string
          notes: string | null
          phone: string | null
          state: string | null
          updated_at: string | null
          utility_company: string | null
          utility_rate: number | null
          zipcode: string | null
        }
        Insert: {
          address?: string | null
          city?: string | null
          created_at?: string | null
          email?: string | null
          estimated_annual_usage_kwh?: number | null
          group_id: string
          id?: string
          name: string
          notes?: string | null
          phone?: string | null
          state?: string | null
          updated_at?: string | null
          utility_company?: string | null
          utility_rate?: number | null
          zipcode?: string | null
        }
        Update: {
          address?: string | null
          city?: string | null
          created_at?: string | null
          email?: string | null
          estimated_annual_usage_kwh?: number | null
          group_id?: string
          id?: string
          name?: string
          notes?: string | null
          phone?: string | null
          state?: string | null
          updated_at?: string | null
          utility_company?: string | null
          utility_rate?: number | null
          zipcode?: string | null
        }
        Relationships: []
      }
      error_logs: {
        Row: {
          context: Json | null
          created_at: string
          error_type: string
          id: string
          message: string
        }
        Insert: {
          context?: Json | null
          created_at?: string
          error_type: string
          id?: string
          message: string
        }
        Update: {
          context?: Json | null
          created_at?: string
          error_type?: string
          id?: string
          message?: string
        }
        Relationships: []
      }
      group_invites: {
        Row: {
          accepted_at: string | null
          created_at: string
          group_id: string
          id: string
          invited_by: string
          roles: string[]
          user_id: string | null
        }
        Insert: {
          accepted_at?: string | null
          created_at?: string
          group_id: string
          id?: string
          invited_by: string
          roles?: string[]
          user_id?: string | null
        }
        Update: {
          accepted_at?: string | null
          created_at?: string
          group_id?: string
          id?: string
          invited_by?: string
          roles?: string[]
          user_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "group_invites_group_id_fkey"
            columns: ["group_id"]
            isOneToOne: false
            referencedRelation: "groups"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "group_invites_group_id_fkey"
            columns: ["group_id"]
            isOneToOne: false
            referencedRelation: "user_organizations"
            referencedColumns: ["group_id"]
          },
        ]
      }
      group_users: {
        Row: {
          created_at: string
          group_id: string
          id: string
          metadata: Json
          role: string
          updated_at: string
          user_id: string
        }
        Insert: {
          created_at?: string
          group_id: string
          id?: string
          metadata?: Json
          role?: string
          updated_at?: string
          user_id: string
        }
        Update: {
          created_at?: string
          group_id?: string
          id?: string
          metadata?: Json
          role?: string
          updated_at?: string
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "group_users_group_id_fkey"
            columns: ["group_id"]
            isOneToOne: false
            referencedRelation: "groups"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "group_users_group_id_fkey"
            columns: ["group_id"]
            isOneToOne: false
            referencedRelation: "user_organizations"
            referencedColumns: ["group_id"]
          },
        ]
      }
      groups: {
        Row: {
          created_at: string
          description: string | null
          id: string
          metadata: Json | null
          name: string | null
          organization_type: string | null
          parent_group_id: string | null
          settings: Json | null
          updated_at: string
        }
        Insert: {
          created_at?: string
          description?: string | null
          id?: string
          metadata?: Json | null
          name?: string | null
          organization_type?: string | null
          parent_group_id?: string | null
          settings?: Json | null
          updated_at?: string
        }
        Update: {
          created_at?: string
          description?: string | null
          id?: string
          metadata?: Json | null
          name?: string | null
          organization_type?: string | null
          parent_group_id?: string | null
          settings?: Json | null
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "groups_parent_group_id_fkey"
            columns: ["parent_group_id"]
            isOneToOne: false
            referencedRelation: "groups"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "groups_parent_group_id_fkey"
            columns: ["parent_group_id"]
            isOneToOne: false
            referencedRelation: "user_organizations"
            referencedColumns: ["group_id"]
          },
        ]
      }
      integration_secrets: {
        Row: {
          created_at: string | null
          encrypted_value: string
          expires_at: string | null
          group_id: string | null
          id: string
          integration_name: string
          is_active: boolean | null
          metadata: Json | null
          secret_type: string
          updated_at: string | null
          user_id: string
        }
        Insert: {
          created_at?: string | null
          encrypted_value: string
          expires_at?: string | null
          group_id?: string | null
          id?: string
          integration_name: string
          is_active?: boolean | null
          metadata?: Json | null
          secret_type: string
          updated_at?: string | null
          user_id: string
        }
        Update: {
          created_at?: string | null
          encrypted_value?: string
          expires_at?: string | null
          group_id?: string | null
          id?: string
          integration_name?: string
          is_active?: boolean | null
          metadata?: Json | null
          secret_type?: string
          updated_at?: string | null
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "integration_secrets_group_id_fkey"
            columns: ["group_id"]
            isOneToOne: false
            referencedRelation: "groups"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "integration_secrets_group_id_fkey"
            columns: ["group_id"]
            isOneToOne: false
            referencedRelation: "user_organizations"
            referencedColumns: ["group_id"]
          },
        ]
      }
      profiles: {
        Row: {
          avatar_url: string | null
          company_name: string | null
          created_at: string
          email: string
          first_name: string | null
          id: string
          last_name: string | null
          updated_at: string
        }
        Insert: {
          avatar_url?: string | null
          company_name?: string | null
          created_at?: string
          email: string
          first_name?: string | null
          id: string
          last_name?: string | null
          updated_at?: string
        }
        Update: {
          avatar_url?: string | null
          company_name?: string | null
          created_at?: string
          email?: string
          first_name?: string | null
          id?: string
          last_name?: string | null
          updated_at?: string
        }
        Relationships: []
      }
      project_stage_logs: {
        Row: {
          entered_at: string | null
          exited_at: string | null
          id: string
          project_id: string
          stage_id: string
        }
        Insert: {
          entered_at?: string | null
          exited_at?: string | null
          id?: string
          project_id: string
          stage_id: string
        }
        Update: {
          entered_at?: string | null
          exited_at?: string | null
          id?: string
          project_id?: string
          stage_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "project_stage_logs_project_id_fkey"
            columns: ["project_id"]
            isOneToOne: false
            referencedRelation: "projects"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "project_stage_logs_stage_id_fkey"
            columns: ["stage_id"]
            isOneToOne: false
            referencedRelation: "workflow_stages"
            referencedColumns: ["id"]
          },
        ]
      }
      projects: {
        Row: {
          address: string
          city: string
          client_email: string | null
          client_id: string | null
          client_name: string | null
          client_phone: string | null
          created_at: string
          group_id: string
          id: string
          input_approx_utility_bill: number | null
          lat: number | null
          lng: number | null
          place_id: string | null
          project_stage_id: string | null
          solar_api_id: string | null
          stage_updated_at: string | null
          state: string | null
          status: string | null
          title: string
          updated_at: string
          utility_rate_kwh: number | null
          workflow_template_id: string | null
          zipcode: string | null
        }
        Insert: {
          address: string
          city: string
          client_email?: string | null
          client_id?: string | null
          client_name?: string | null
          client_phone?: string | null
          created_at?: string
          group_id: string
          id?: string
          input_approx_utility_bill?: number | null
          lat?: number | null
          lng?: number | null
          place_id?: string | null
          project_stage_id?: string | null
          solar_api_id?: string | null
          stage_updated_at?: string | null
          state?: string | null
          status?: string | null
          title: string
          updated_at?: string
          utility_rate_kwh?: number | null
          workflow_template_id?: string | null
          zipcode?: string | null
        }
        Update: {
          address?: string
          city?: string
          client_email?: string | null
          client_id?: string | null
          client_name?: string | null
          client_phone?: string | null
          created_at?: string
          group_id?: string
          id?: string
          input_approx_utility_bill?: number | null
          lat?: number | null
          lng?: number | null
          place_id?: string | null
          project_stage_id?: string | null
          solar_api_id?: string | null
          stage_updated_at?: string | null
          state?: string | null
          status?: string | null
          title?: string
          updated_at?: string
          utility_rate_kwh?: number | null
          workflow_template_id?: string | null
          zipcode?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "projects_client_id_fkey"
            columns: ["client_id"]
            isOneToOne: false
            referencedRelation: "clients"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "projects_project_stage_id_fkey"
            columns: ["project_stage_id"]
            isOneToOne: false
            referencedRelation: "workflow_stages"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "projects_workflow_template_id_fkey"
            columns: ["workflow_template_id"]
            isOneToOne: false
            referencedRelation: "workflow_templates"
            referencedColumns: ["id"]
          },
        ]
      }
      proposal_stage_logs: {
        Row: {
          entered_at: string | null
          exited_at: string | null
          id: string
          proposal_id: string
          stage_id: string
        }
        Insert: {
          entered_at?: string | null
          exited_at?: string | null
          id?: string
          proposal_id: string
          stage_id: string
        }
        Update: {
          entered_at?: string | null
          exited_at?: string | null
          id?: string
          proposal_id?: string
          stage_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "proposal_stage_logs_proposal_id_fkey"
            columns: ["proposal_id"]
            isOneToOne: false
            referencedRelation: "proposals"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "proposal_stage_logs_stage_id_fkey"
            columns: ["stage_id"]
            isOneToOne: false
            referencedRelation: "workflow_stages"
            referencedColumns: ["id"]
          },
        ]
      }
      proposals: {
        Row: {
          assessment_id: string | null
          client_id: string | null
          content: Json | null
          created_at: string | null
          group_id: string
          id: string
          is_complete: boolean | null
          missing_data: string[] | null
          project_id: string
          proposal_stage_id: string | null
          title: string
          updated_at: string | null
          workflow_template_id: string | null
        }
        Insert: {
          assessment_id?: string | null
          client_id?: string | null
          content?: Json | null
          created_at?: string | null
          group_id: string
          id?: string
          is_complete?: boolean | null
          missing_data?: string[] | null
          project_id: string
          proposal_stage_id?: string | null
          title: string
          updated_at?: string | null
          workflow_template_id?: string | null
        }
        Update: {
          assessment_id?: string | null
          client_id?: string | null
          content?: Json | null
          created_at?: string | null
          group_id?: string
          id?: string
          is_complete?: boolean | null
          missing_data?: string[] | null
          project_id?: string
          proposal_stage_id?: string | null
          title?: string
          updated_at?: string | null
          workflow_template_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "proposals_assessment_id_fkey"
            columns: ["assessment_id"]
            isOneToOne: false
            referencedRelation: "solar_assessments"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "proposals_client_id_fkey"
            columns: ["client_id"]
            isOneToOne: false
            referencedRelation: "clients"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "proposals_project_id_fkey"
            columns: ["project_id"]
            isOneToOne: false
            referencedRelation: "projects"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "proposals_proposal_stage_id_fkey"
            columns: ["proposal_stage_id"]
            isOneToOne: false
            referencedRelation: "workflow_stages"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "proposals_workflow_template_id_fkey"
            columns: ["workflow_template_id"]
            isOneToOne: false
            referencedRelation: "workflow_templates"
            referencedColumns: ["id"]
          },
        ]
      }
      rbac_error_logs: {
        Row: {
          context: Json | null
          created_at: string
          error_type: string
          id: string
          message: string
        }
        Insert: {
          context?: Json | null
          created_at?: string
          error_type: string
          id?: string
          message: string
        }
        Update: {
          context?: Json | null
          created_at?: string
          error_type?: string
          id?: string
          message?: string
        }
        Relationships: []
      }
      sensitive_data: {
        Row: {
          created_at: string
          data: string
          id: string
          owned_by_group: string
        }
        Insert: {
          created_at?: string
          data?: string
          id?: string
          owned_by_group: string
        }
        Update: {
          created_at?: string
          data?: string
          id?: string
          owned_by_group?: string
        }
        Relationships: []
      }
      solar_assessments: {
        Row: {
          assessment_stage_id: string | null
          building_insights: Json | null
          created_at: string | null
          derived_monthly_bill_for_selected_config: number | null
          dsm_url: string | null
          flux_composite_gif_url: string | null
          flux_overlay_url: string | null
          group_id: string
          id: string
          input_approx_utility_bill: number | null
          mask_url: string | null
          monthly_composite_flux_urls: string[] | null
          monthly_flux_urls: string[] | null
          optimal_configuration: Json | null
          project_id: string
          rgb_url: string | null
          selected_panel_config_index: number | null
          status: string | null
          supabase_path_root: string | null
          updated_at: string | null
          version_number: number | null
          workflow_template_id: string | null
        }
        Insert: {
          assessment_stage_id?: string | null
          building_insights?: Json | null
          created_at?: string | null
          derived_monthly_bill_for_selected_config?: number | null
          dsm_url?: string | null
          flux_composite_gif_url?: string | null
          flux_overlay_url?: string | null
          group_id: string
          id?: string
          input_approx_utility_bill?: number | null
          mask_url?: string | null
          monthly_composite_flux_urls?: string[] | null
          monthly_flux_urls?: string[] | null
          optimal_configuration?: Json | null
          project_id: string
          rgb_url?: string | null
          selected_panel_config_index?: number | null
          status?: string | null
          supabase_path_root?: string | null
          updated_at?: string | null
          version_number?: number | null
          workflow_template_id?: string | null
        }
        Update: {
          assessment_stage_id?: string | null
          building_insights?: Json | null
          created_at?: string | null
          derived_monthly_bill_for_selected_config?: number | null
          dsm_url?: string | null
          flux_composite_gif_url?: string | null
          flux_overlay_url?: string | null
          group_id?: string
          id?: string
          input_approx_utility_bill?: number | null
          mask_url?: string | null
          monthly_composite_flux_urls?: string[] | null
          monthly_flux_urls?: string[] | null
          optimal_configuration?: Json | null
          project_id?: string
          rgb_url?: string | null
          selected_panel_config_index?: number | null
          status?: string | null
          supabase_path_root?: string | null
          updated_at?: string | null
          version_number?: number | null
          workflow_template_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "solar_assessments_assessment_stage_id_fkey"
            columns: ["assessment_stage_id"]
            isOneToOne: false
            referencedRelation: "workflow_stages"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "solar_assessments_project_id_fkey"
            columns: ["project_id"]
            isOneToOne: false
            referencedRelation: "projects"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "solar_assessments_workflow_template_id_fkey"
            columns: ["workflow_template_id"]
            isOneToOne: false
            referencedRelation: "workflow_templates"
            referencedColumns: ["id"]
          },
        ]
      }
      solar_incentives: {
        Row: {
          amount: number | null
          amount_type: string | null
          applicable_states: string[] | null
          applicable_zipcodes: string[] | null
          created_at: string | null
          description: string | null
          expires_at: string | null
          group_id: string | null
          id: string
          is_active: boolean | null
          max_amount: number | null
          name: string
          tags: string[] | null
          type: string | null
          updated_at: string | null
        }
        Insert: {
          amount?: number | null
          amount_type?: string | null
          applicable_states?: string[] | null
          applicable_zipcodes?: string[] | null
          created_at?: string | null
          description?: string | null
          expires_at?: string | null
          group_id?: string | null
          id?: string
          is_active?: boolean | null
          max_amount?: number | null
          name: string
          tags?: string[] | null
          type?: string | null
          updated_at?: string | null
        }
        Update: {
          amount?: number | null
          amount_type?: string | null
          applicable_states?: string[] | null
          applicable_zipcodes?: string[] | null
          created_at?: string | null
          description?: string | null
          expires_at?: string | null
          group_id?: string | null
          id?: string
          is_active?: boolean | null
          max_amount?: number | null
          name?: string
          tags?: string[] | null
          type?: string | null
          updated_at?: string | null
        }
        Relationships: []
      }
      vendor_settings: {
        Row: {
          branding: Json | null
          created_at: string | null
          group_id: string
          id: string
          incentives: Json | null
          panel_types: Json | null
          pricing: Json | null
          updated_at: string | null
        }
        Insert: {
          branding?: Json | null
          created_at?: string | null
          group_id: string
          id?: string
          incentives?: Json | null
          panel_types?: Json | null
          pricing?: Json | null
          updated_at?: string | null
        }
        Update: {
          branding?: Json | null
          created_at?: string | null
          group_id?: string
          id?: string
          incentives?: Json | null
          panel_types?: Json | null
          pricing?: Json | null
          updated_at?: string | null
        }
        Relationships: []
      }
      workflow_stages: {
        Row: {
          color: string | null
          created_at: string | null
          id: string
          is_terminal: boolean | null
          label: string
          position: number
          slug: string
          template_id: string
        }
        Insert: {
          color?: string | null
          created_at?: string | null
          id?: string
          is_terminal?: boolean | null
          label: string
          position: number
          slug: string
          template_id: string
        }
        Update: {
          color?: string | null
          created_at?: string | null
          id?: string
          is_terminal?: boolean | null
          label?: string
          position?: number
          slug?: string
          template_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "workflow_stages_template_id_fkey"
            columns: ["template_id"]
            isOneToOne: false
            referencedRelation: "workflow_templates"
            referencedColumns: ["id"]
          },
        ]
      }
      workflow_templates: {
        Row: {
          created_at: string | null
          default_template: boolean | null
          group_id: string | null
          id: string
          name: string
          type: string
        }
        Insert: {
          created_at?: string | null
          default_template?: boolean | null
          group_id?: string | null
          id?: string
          name: string
          type: string
        }
        Update: {
          created_at?: string | null
          default_template?: boolean | null
          group_id?: string | null
          id?: string
          name?: string
          type?: string
        }
        Relationships: []
      }
    }
    Views: {
      role_summary: {
        Row: {
          assignment_count: number | null
          role: string | null
          total_groups: number | null
          total_users: number | null
        }
        Relationships: []
      }
      user_organizations: {
        Row: {
          created_at: string | null
          group_id: string | null
          is_parent_org: boolean | null
          is_sub_account: boolean | null
          organization_description: string | null
          organization_name: string | null
          organization_type: string | null
          parent_group_id: string | null
          parent_organization_name: string | null
          parent_organization_type: string | null
          role_metadata: Json | null
          user_id: string | null
          user_role: string | null
        }
        Relationships: [
          {
            foreignKeyName: "groups_parent_group_id_fkey"
            columns: ["parent_group_id"]
            isOneToOne: false
            referencedRelation: "groups"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "groups_parent_group_id_fkey"
            columns: ["parent_group_id"]
            isOneToOne: false
            referencedRelation: "user_organizations"
            referencedColumns: ["group_id"]
          },
        ]
      }
      user_role_view: {
        Row: {
          email: string | null
          first_name: string | null
          group_id: string | null
          group_metadata: Json | null
          last_name: string | null
          role: string | null
          user_id: string | null
        }
        Relationships: [
          {
            foreignKeyName: "group_users_group_id_fkey"
            columns: ["group_id"]
            isOneToOne: false
            referencedRelation: "groups"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "group_users_group_id_fkey"
            columns: ["group_id"]
            isOneToOne: false
            referencedRelation: "user_organizations"
            referencedColumns: ["group_id"]
          },
        ]
      }
      user_roles_view: {
        Row: {
          first_name: string | null
          group_id: string | null
          group_metadata: Json | null
          last_name: string | null
          role: string | null
          user_email: string | null
          user_id: string | null
        }
        Relationships: [
          {
            foreignKeyName: "group_users_group_id_fkey"
            columns: ["group_id"]
            isOneToOne: false
            referencedRelation: "groups"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "group_users_group_id_fkey"
            columns: ["group_id"]
            isOneToOne: false
            referencedRelation: "user_organizations"
            referencedColumns: ["group_id"]
          },
        ]
      }
    }
    Functions: {
      assign_default_roles: {
        Args: { user_id: string; group_id: string; role_type: string }
        Returns: undefined
      }
      check_rate_limit: {
        Args: {
          action_type: string
          user_id?: string
          time_window?: unknown
          max_attempts?: number
        }
        Returns: boolean
      }
      create_organization: {
        Args: {
          org_name: string
          org_type?: string
          org_description?: string
          creator_role?: string
        }
        Returns: Json
      }
      create_sub_account: {
        Args: {
          parent_group_id: string
          sub_account_name: string
          sub_account_description?: string
          admin_user_id?: string
        }
        Returns: Json
      }
      create_test_group: {
        Args: Record<PropertyKey, never>
        Returns: string
      }
      db_pre_request: {
        Args: Record<PropertyKey, never>
        Returns: Json
      }
      db_pre_request_deprec: {
        Args: Record<PropertyKey, never>
        Returns: Json
      }
      db_pre_request_less_old: {
        Args: Record<PropertyKey, never>
        Returns: Json
      }
      db_pre_request_old: {
        Args: Record<PropertyKey, never>
        Returns: undefined
      }
      debug_create_organization: {
        Args: { org_name: string; org_type?: string }
        Returns: string
      }
      decrypt_integration_secret: {
        Args: { encrypted_value: string }
        Returns: string
      }
      encrypt_integration_secret: {
        Args: { secret_value: string }
        Returns: string
      }
      get_safe_user_claims: {
        Args: Record<PropertyKey, never>
        Returns: Json
      }
      get_user_claims: {
        Args: Record<PropertyKey, never>
        Returns: Json
      }
      get_user_onboarding_status: {
        Args: { user_uuid?: string }
        Returns: Json
      }
      get_user_profile: {
        Args: { target_user_id?: string }
        Returns: Json
      }
      has_permission: {
        Args: { group_id: string; role: string }
        Returns: boolean
      }
      invite_user_to_organization: {
        Args: {
          group_id: string
          user_email: string
          user_role?: string
          invitation_message?: string
        }
        Returns: Json
      }
      jwt_is_expired: {
        Args: Record<PropertyKey, never>
        Returns: boolean
      }
      log_permission_check: {
        Args: {
          permission_type: string
          result: boolean
          duration_ms: number
          details?: Json
        }
        Returns: undefined
      }
      log_rbac_errors: {
        Args: { error_message: string; context_data?: Json }
        Returns: undefined
      }
      log_security_event: {
        Args: { event_type: string; user_id?: string; details?: Json }
        Returns: undefined
      }
      migrate_to_new_role_names: {
        Args: Record<PropertyKey, never>
        Returns: undefined
      }
      safe_user_has_group_role: {
        Args: { group_id: string; group_role: string }
        Returns: boolean
      }
      seed_test_group: {
        Args: Record<PropertyKey, never>
        Returns: string
      }
      store_integration_secret: {
        Args: {
          integration_name: string
          secret_type: string
          secret_value: string
          target_group_id?: string
          secret_metadata?: Json
          expires_at?: string
        }
        Returns: Json
      }
      test_permission_check: {
        Args: {
          test_user_id: string
          test_group_id: string
          test_permission: string
        }
        Returns: {
          method: string
          result: boolean
        }[]
      }
      update_user_profile: {
        Args: { profile_updates: Json }
        Returns: Json
      }
      user_has_group_role: {
        Args: { group_id: string; group_role: string }
        Returns: boolean
      }
      user_has_permission: {
        Args: { group_id: string; permission: string }
        Returns: boolean
      }
      user_is_group_member: {
        Args: { group_id: string }
        Returns: boolean
      }
      validate_email: {
        Args: { email: string }
        Returns: boolean
      }
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  graphql_public: {
    Enums: {},
  },
  public: {
    Enums: {},
  },
} as const
